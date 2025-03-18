# treasures/views.py
import csv
import logging
import random
import re

from NihongoDekita import settings

logger = logging.getLogger(__name__)

from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from datetime import timedelta, datetime
from .models import UserProgress, DailyWord, Kanji, QuizQuestion, DailyKanji
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from .models import UserProfile

def home(request):
    today = timezone.now().date()
    daily_word = DailyWord.objects.filter(date=today).first()

    # Fallback: If no word for today, get the earliest word and reuse it
    if not daily_word:
        daily_word = DailyWord.objects.order_by('date').first()

    context = {
        'daily_word': daily_word,
    }
    return render(request, 'home.html', context)

def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context = {
        'user': request.user,
    }
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
    return render(request, 'kanji/n5_kanji.html')


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
    auth_logout(request)
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
        token = default_token_generator.make_token(user)  # Use Django's token generator
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

        # Log out the user to ensure they are not automatically logged in
        auth_logout(request)
        # Set the success message
        messages.success(request, "Registration successful! Please check your email to confirm your account.")
        # Redirect to the login page
        return redirect('login')  # Use namespaced URL to avoid conflicts

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
            profile.user.is_active = True
            profile.user.save()
            profile.save()
            messages.success(request, "Email confirmed! You can now log in.")
            # Updated message with a clickable link
            message = (
                'Email confirmed! You will be redirected to the login page in 3 seconds. '
                'If not redirected, <a href="' + reverse('login') + '" class="text-primary">click here to go to the login page</a>.'
            )
            return render(request, 'registration/confirm_email.html', {'message': message})
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
    if request.method == "POST":
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            profile = user.profile
            if user.is_active:
                messages.info(request, "This account is already verified.")
            else:
                # Check if a confirmation email was sent recently (within 5 minutes)
                if hasattr(profile, 'last_confirmation_sent') and (timezone.now() - profile.last_confirmation_sent).total_seconds() < 300:  # 300 seconds = 5 minutes
                    messages.warning(request, "A verification email was sent recently. Please wait 5 minutes before requesting another.")
                else:
                    # Generate a new token and update the profile
                    token = default_token_generator.make_token(user)
                    profile.confirmation_token = token
                    profile.last_confirmation_sent = timezone.now()  # Track the last sent time
                    profile.save()

                    # Send confirmation email
                    confirmation_url = request.build_absolute_uri(reverse('confirm_email', kwargs={'token': token}))
                    subject = 'Resend Verify Your NihongoDekita Account'
                    message = f'Hi {user.username},\n\nPlease confirm your email by clicking the link below:\n{confirmation_url}\n\nThank you for using NihongoDekita!'
                    send_mail(
                        subject,
                        message,
                        settings.EMAIL_HOST_USER,
                        [email],
                        fail_silently=False,
                    )
                    messages.success(request, "A verification link has been sent. Please check your inbox and spam folder. If not received in 5 minutes, resend again.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist in our system.")
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile not found. Please contact support.")
        return render(request, 'registration/resend_confirmation.html')

    return render(request, 'registration/resend_confirmation.html')

class CustomPasswordResetView(PasswordResetView):
    template_name = 'registration/password_reset_form.html'
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            messages.error(self.request, "This email is not registered with us.")
            return self.render_to_response(self.get_context_data(form=form))
        return super().form_valid(form)

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
            recipient_list = ['veerababusaviti2103@gmail.com']  # Your email

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

@login_required
def admin_bulk_upload(request):
    if not request.user.is_superuser:
        messages.error(request, "Only admins can access this page.")
        return redirect('home')

    if request.method == "POST":
        # Handle DailyWord upload
        if 'dailyword_csv' in request.FILES:
            csv_file = request.FILES['dailyword_csv']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a CSV file for Daily Words.")
                return redirect('admin_bulk_upload')

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            required_headers = {"word", "reading", "english_meaning"}
            has_date = "date" in reader.fieldnames
            if not required_headers.issubset(reader.fieldnames):
                messages.error(request, "DailyWord CSV must have headers: word, reading, english_meaning (date optional)")
                return redirect('admin_bulk_upload')

            current_date = timezone.now().date()
            for i, row in enumerate(reader):
                try:
                    date = datetime.strptime(row["date"], "%Y-%m-%d").date() if has_date else current_date + timedelta(days=i)
                    DailyWord.objects.update_or_create(
                        date=date,
                        defaults={
                            "word": row["word"],
                            "reading": row["reading"],
                            "english_meaning": row["english_meaning"],
                        }
                    )
                except Exception as e:
                    messages.error(request, f"DailyWord row {i+1}: {str(e)}")
            messages.success(request, "Daily Words uploaded successfully!")

        # Handle Kanji upload
        elif 'kanji_csv' in request.FILES:
            csv_file = request.FILES['kanji_csv']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a CSV file for Kanji.")
                return redirect('admin_bulk_upload')

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            required_headers = {"character", "level", "on_reading", "kun_reading", "meaning", "stroke_count"}
            if not required_headers.issubset(reader.fieldnames):
                messages.error(request, "Kanji CSV must have headers: character, level, on_reading, kun_reading, meaning, stroke_count")
                return redirect('admin_bulk_upload')

            for i, row in enumerate(reader):
                try:
                    Kanji.objects.update_or_create(
                        character=row["character"],
                        level=row["level"],
                        defaults={
                            "on_reading": row["on_reading"],
                            "kun_reading": row["kun_reading"],
                            "meaning": row["meaning"],
                            "stroke_count": int(row["stroke_count"]),
                        }
                    )
                except Exception as e:
                    messages.error(request, f"Kanji row {i+1}: {str(e)}")
            messages.success(request, "Kanji uploaded successfully!")

        # Handle QuizQuestion upload
        elif 'quiz_csv' in request.FILES:
            csv_file = request.FILES['quiz_csv']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Please upload a CSV file for Quiz Questions.")
                return redirect('admin_bulk_upload')

            decoded_file = csv_file.read().decode("utf-8").splitlines()
            reader = csv.DictReader(decoded_file)
            required_headers = {"level", "question", "wrong_answer1", "wrong_answer2", "wrong_answer3", "correct_answer"}
            if not required_headers.issubset(reader.fieldnames):
                messages.error(request, "Quiz CSV must have headers: level, question, wrong_answer1, wrong_answer2, wrong_answer3, correct_answer")
                return redirect('admin_bulk_upload')

            for i, row in enumerate(reader):
                try:
                    QuizQuestion.objects.update_or_create(
                        level=row["level"],
                        question=row["question"],
                        defaults={
                            "wrong_answer1": row["wrong_answer1"],
                            "wrong_answer2": row["wrong_answer2"],
                            "wrong_answer3": row["wrong_answer3"],
                            "correct_answer": row["correct_answer"],
                        }
                    )
                except Exception as e:
                    messages.error(request, f"Quiz row {i+1}: {str(e)}")
            messages.success(request, "Quiz Questions uploaded successfully!")

        return redirect('admin_bulk_upload')

    return render(request, 'admin_bulk_upload.html')