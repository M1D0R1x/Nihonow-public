# treasures/views.py
import logging
import random
import re
import uuid

logger = logging.getLogger(__name__)

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.urls import reverse
from django.db.models import Q  # Add this import to fix the unresolved reference

from .models import UserProfile
from .models import QuizQuestion, UserProgress

from django.utils import timezone
from django.shortcuts import render
from .models import DailyWord


def home(request):
    # Use timezone-aware current date
    today = timezone.now().date()
    daily_word = DailyWord.objects.filter(date=today).first()

    context = {
        'daily_word': daily_word,
    }
    return render(request, 'home.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    email_confirmed = getattr(request.user.profile, 'email_confirmed', False) if hasattr(request.user, 'profile') else False
    context = {
        'user': request.user,
        'email_confirmed': email_confirmed,
    }
    if not email_confirmed:
        messages.warning(request, "Please verify your email to access all features. Check your inbox or <a href='{% url 'resend_confirmation' %}'>resend confirmation</a>.")
    return render(request, 'profile.html', context)

def numbers(request):
    return render(request, 'numbers.html')

def hiragana(request):
    return render(request, 'hiragana.html')

def katakana(request):
    return render(request, 'katakana.html')

def n5(request):
    return render(request, 'level_detail.html', {'level': 'N5'})
def n5_quiz(request):
    return render(request, 'quiz.html', {'level': 'N5'})
def n5_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N5'})

def n4(request):
    return render(request, 'level_detail.html', {'level': 'N4'})
def n4_quiz(request):
    return render(request, 'quiz.html', {'level': 'N4'})
def n4_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N4'})

def n3(request):
    return render(request, 'level_detail.html', {'level': 'N3'})
def n3_quiz(request):
    return render(request, 'quiz.html', {'level': 'N3'})
def n3_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N3'})

def n2(request):
    return render(request, 'level_detail.html', {'level': 'N2'})
def n2_quiz(request):
    return render(request, 'quiz.html', {'level': 'N2'})
def n2_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N2'})

def n1(request):
    return render(request, 'level_detail.html', {'level': 'N1'})
def n1_quiz(request):
    return render(request, 'quiz.html', {'level': 'N1'})
def n1_kanji(request):
    return render(request, 'kanji_list.html', {'level': 'N1'})

def about(request):
    return render(request, 'about.html')

def resources(request):
    return render(request, 'resources.html')

def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to home page after logout

@login_required
def dashboard(request):
    average_progress = 0
    if request.user.is_authenticated:
        user_progress = UserProgress.objects.filter(user=request.user)
        if user_progress.exists():
            total_score = sum(up.quiz_score for up in user_progress if up.quiz_score is not None)
            count = user_progress.count()
            average_progress = total_score / count if count > 0 else 0

    context = {
        'average_progress': average_progress,
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Password validation
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'registration/register.html')

        if len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters long.")
            return render(request, 'registration/register.html')

        if not re.search(r'\d', password1):
            messages.error(request, "Password must contain at least one number.")
            return render(request, 'registration/register.html')

        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password1):
            messages.error(request, "Password must contain at least one special character (e.g., !@#$%^&*).")
            return render(request, 'registration/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'registration/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, 'registration/register.html')

        # Create the user, but set is_active to False until email is confirmed
        user = User.objects.create_user(username=username, email=email, password=password1, is_active=False)
        user.save()

        # Create a user profile with a confirmation token
        token = str(uuid.uuid4())
        UserProfile.objects.create(user=user, confirmation_token=token)

        # Send confirmation email
        confirmation_url = request.build_absolute_uri(reverse('confirm_email', kwargs={'token': token}))
        subject = 'Confirm Your Email for NihongoDekita'
        message = f'Hi {username},\n\nPlease confirm your email by clicking the link below:\n{confirmation_url}\n\nThank you for joining NihongoDekita!'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )

        messages.success(request, "Registration successful! Please check your email to confirm your account.")
        return redirect('login')

    return render(request, 'registration/register.html')

def confirm_email(request, token):
    logger.info(f"Attempting to confirm email with token: {token}")
    try:
        profile = UserProfile.objects.get(confirmation_token=token)
        logger.info(f"Found profile for user: {profile.user.username}")
        if profile.email_confirmed:
            messages.info(request, "Your email is already confirmed.")
        else:
            profile.email_confirmed = True
            profile.confirmation_token = None  # Clear the token
            profile.save()
            profile.user.is_active = True
            profile.user.save()
            messages.success(request, "Email confirmed! You can now log in.")
    except UserProfile.DoesNotExist:
        logger.error(f"Invalid confirmation token: {token}")
        messages.error(request, "Invalid confirmation link.")
    return redirect('login')

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('dashboard')
        else:
            try:
                user = User.objects.get(Q(username=username) | Q(email=username))
                if hasattr(user, 'profile') and not user.profile.email_confirmed:
                    messages.error(request, "Please confirm your email to log in. Check your inbox for the confirmation link.")
                else:
                    messages.error(request, "Invalid email/username or password.")
            except User.DoesNotExist:
                messages.error(request, "Invalid email/username or password.")
    return render(request, 'registration/login.html')

def resend_confirmation(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Check if user has a profile, create one if not
            if not hasattr(user, 'profile'):
                UserProfile.objects.create(user=user, email_confirmed=False, confirmation_token=None)
            if not user.profile.email_confirmed:
                token = str(uuid.uuid4())
                user.profile.confirmation_token = token
                user.profile.save()

                confirmation_url = request.build_absolute_uri(reverse('confirm_email', kwargs={'token': token}))
                subject = 'Resend: Confirm Your Email for NihongoDekita'
                message = f'Hi {user.username},\n\nPlease confirm your email by clicking the link below:\n{confirmation_url}\n\nThank you for joining NihongoDekita!'
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, "Confirmation email resent. Please check your inbox.")
            else:
                messages.info(request, "Your email is already confirmed.")
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
    return render(request, 'registration/resend_confirmation.html')

def contact(request):
    submitted = False
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Validate the form data
        if not name or not email or not message:
            messages.error(request, 'Please fill out all fields.')
        else:
            # Prepare the email content
            subject = f'New Contact Form Submission from {name}'
            message_body = f'Name: {name}\nEmail: {email}\n\nMessage:\n{message}'
            from_email = settings.EMAIL_HOST_USER
            recipient_list = ['veerababusaviti21@gmail.com']  # Your email

            try:
                # Send the email
                send_mail(
                    subject,
                    message_body,
                    from_email,
                    recipient_list,
                    fail_silently=False,
                )
                submitted = True  # Set submitted to True for confirmation
            except Exception as e:
                messages.error(request, f'Failed to send message. Error: {str(e)}')

    return render(request, 'contact.html', {'submitted': submitted})

def quiz(request, level):
    if not request.user.is_authenticated:
        return redirect('login')

    questions = QuizQuestion.objects.filter(level=level)
    if not questions:
        return render(request, 'quiz.html', {'level': level, 'error': 'No questions available for this level.'})

    if request.method == 'POST':
        score = 0
        total = questions.count()
        for question in questions:
            selected = request.POST.get(f'question_{question.id}')
            if selected == question.correct_answer:
                score += 1

        percentage = (score / total) * 100
        progress, created = UserProgress.objects.get_or_create(user=request.user, level=level)
        progress.quiz_score = percentage
        progress.save()

        return render(request, 'quiz.html', {'level': level, 'submitted': True, 'score': percentage})

    # Prepare questions with shuffled options
    questions_with_options = []
    for question in questions:
        options = [question.wrong_answer1, question.wrong_answer2, question.wrong_answer3, question.correct_answer]
        random.shuffle(options)  # Shuffle the options
        questions_with_options.append({
            'question': question,
            'options': options,
        })

    return render(request, 'quiz.html', {'level': level, 'questions_with_options': questions_with_options})
