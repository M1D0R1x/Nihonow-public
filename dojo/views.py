from ably import AblyRest
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import DojoRoom, DojoParticipant
import json
import random
from django.conf import settings
from .data.hiragana import HIRAGANA_QUESTIONS
from .data.katakana import KATAKANA_QUESTIONS
from .data.kanji_n5 import KANJI_N5_QUESTIONS
from .data.blank_data.hiragana import HIRAGANA_BLANK_QUESTIONS
from .data.blank_data.katakana import KATAKANA_BLANK_QUESTIONS
from .data.blank_data.kanji_n5 import KANJI_N5_BLANK_QUESTIONS


@login_required
def dojo_home(request):
    """Home page for the Dojo feature"""
    return render(request, 'dojo/dojo_home.html')


@login_required
def create_room(request):
    """Create a new room as a host"""
    if request.method == 'POST':
        room_name = request.POST.get('room_name', f"{request.user.username}'s Room")
        category = request.POST.get('category')
        subcategory = request.POST.get('subcategory')
        question_type = request.POST.get('question_type')
        time_limit = request.POST.get('time_limit', 60)

        room = DojoRoom.objects.create(
            host=request.user,
            name=room_name,
            category=category,
            subcategory=subcategory,
            question_type=question_type,
            time_limit=time_limit
        )
        return redirect('host_room', room_code=room.code)
    return render(request, 'dojo/create_room.html')


@login_required
def host_room(request, room_code):
    """Host view for managing a room"""
    room = get_object_or_404(DojoRoom, code=room_code, host=request.user)
    participants = room.participants.all().order_by('-score')

    context = {
        'room': room,
        'participants': participants,
        'ably_api_key': settings.ABLY_API_KEY,
    }
    return render(request, 'dojo/host_room.html', context)


@login_required
def join_room(request):
    """Join an existing room as a participant"""
    if request.method == 'POST':
        room_code = request.POST.get('room_code')
        try:
            room = DojoRoom.objects.get(code=room_code, is_active=True)

            # Check if user is already a participant
            participant, created = DojoParticipant.objects.get_or_create(
                room=room,
                user=request.user
            )

            return redirect('participant_room', room_code=room.code)
        except DojoRoom.DoesNotExist:
            return render(request, 'dojo/join_room.html', {'error': 'Invalid room code'})

    return render(request, 'dojo/join_room.html')


@login_required
def participant_room(request, room_code):
    """Participant view for a room"""
    room = get_object_or_404(DojoRoom, code=room_code, is_active=True)
    participant = get_object_or_404(DojoParticipant, room=room, user=request.user)

    context = {
        'room': room,
        'participant': participant,
        'ably_api_key': settings.ABLY_API_KEY,
    }
    return render(request, 'dojo/participant_room.html', context)


@csrf_exempt
@login_required
def start_competition(request, room_code):
    """Start the competition (host only)"""
    if request.method == 'POST':
        room = get_object_or_404(DojoRoom, code=room_code, host=request.user)

        # Prepare room settings to send to participants
        room_settings = {
            'category': room.category,
            'subcategory': room.subcategory,
            'question_type': room.question_type,
            'time_limit': room.time_limit,
        }

        room.has_started = True
        room.save()

        # Publish the competition status with settings
        ably = AblyRest(settings.ABLY_API_KEY)
        channel = ably.channels.get(f'dojo-room-{room_code}')
        channel.publish('competition-status', {
            'status': 'started',
            'settings': room_settings
        })

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
@login_required
def end_competition(request, room_code):
    """End the competition (host only)"""
    if request.method == 'POST':
        room = get_object_or_404(DojoRoom, code=room_code, host=request.user)
        room.has_ended = True
        room.is_active = False
        room.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@csrf_exempt
@login_required
def update_score(request, room_code):
    """Update a participant's score"""
    if request.method == 'POST':
        data = json.loads(request.body)
        score = data.get('score', 0)

        room = get_object_or_404(DojoRoom, code=room_code)
        participant = get_object_or_404(DojoParticipant, room=room, user=request.user)

        participant.score = score
        participant.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def leaderboard(request, room_code):
    """API endpoint to get the leaderboard for a room"""
    room = get_object_or_404(DojoRoom, code=room_code)
    participants = room.participants.all().order_by('-score')

    data = []
    for participant in participants:
        data.append({
            'id': participant.id,
            'username': participant.user.username,
            'score': participant.score
        })

    return JsonResponse(data, safe=False)


@login_required
def get_questions(request):
    """API endpoint to get questions based on category, subcategory, and type"""
    category = request.GET.get('category')
    subcategory = request.GET.get('subcategory')
    question_type = request.GET.get('question_type')

    if not category or not subcategory:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Get appropriate question set based on type and category
    if question_type == 'blank':
        if category == 'hiragana':
            questions = HIRAGANA_BLANK_QUESTIONS.get(subcategory, [])
        elif category == 'katakana':
            questions = KATAKANA_BLANK_QUESTIONS.get(subcategory, [])
        elif category == 'kanji':
            questions = KANJI_N5_BLANK_QUESTIONS.get(subcategory, [])
        else:
            questions = []
    else:  # mcq
        if category == 'hiragana':
            questions = HIRAGANA_QUESTIONS.get(subcategory, [])
        elif category == 'katakana':
            questions = KATAKANA_QUESTIONS.get(subcategory, [])
        elif category == 'kanji':
            questions = KANJI_N5_QUESTIONS.get(subcategory, [])
        else:
            questions = []

    return JsonResponse({'questions': questions})

