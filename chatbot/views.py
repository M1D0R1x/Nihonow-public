# chatbot/views.py
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render
from .bot import get_chatbot_response
from .models import ChatLog

def chat_page(request):
    # Pass authentication status to the template
    return render(request, 'chatbot/chat.html', {'is_authenticated': request.user.is_authenticated})

@login_required(login_url='login')
def nihonbot_view(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '').strip()
        if not user_input:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Get response from the chatbot
        response = get_chatbot_response(user_input)

        # Log the conversation
        ChatLog.objects.create(
            user=request.user,
            user_input=user_input,
            bot_response=response
        )

        return JsonResponse({'response': response})

    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required(login_url='login')
def chat_history(request):
    if request.method == 'GET':
        # Get the last 10 conversations for the current user
        history = ChatLog.objects.filter(user=request.user).order_by('-timestamp')[:10]

        # Format the history as a list of dictionaries
        history_list = [
            {
                'user_input': log.user_input,
                'bot_response': log.bot_response,
                'timestamp': log.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for log in history
        ]

        return JsonResponse({'history': history_list})

    return JsonResponse({'error': 'Invalid request'}, status=400)