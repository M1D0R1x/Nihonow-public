from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Vocabulary, QuizQuestion, Kanji, UserProgress

def home(request):
    levels = Vocabulary.LEVEL_CHOICES
    return render(request, 'home.html', {'levels': levels})

def level_detail(request, level):
    vocab_list = Vocabulary.objects.filter(level=level)
    return render(request, 'level_detail.html', {'level': level, 'vocab_list': vocab_list})

def quiz(request, level):
    questions = QuizQuestion.objects.filter(level=level)
    if request.method == 'POST':
        score = 0
        total = questions.count()
        results = []
        for question in questions:
            user_answer = request.POST.get(f'answer_{question.id}')
            is_correct = user_answer == question.correct_answer
            if is_correct:
                score += 1
            results.append({
                'question': question.question,
                'user_answer': user_answer,
                'correct_answer': question.correct_answer,
                'is_correct': is_correct,
            })
        # Mark quiz as completed for the user
        if request.user.is_authenticated:
            UserProgress.objects.update_or_create(
                user=request.user,
                level=level,
                defaults={'quiz_completed': True}
            )
        return render(request, 'quiz_results.html', {
            'level': level,
            'score': score,
            'total': total,
            'results': results,
        })
    # Mark level as studied when user views the quiz
    if request.user.is_authenticated:
        UserProgress.objects.update_or_create(
            user=request.user,
            level=level,
            defaults={'studied': True}
        )
    return render(request, 'quiz.html', {'level': level, 'questions': questions})

def kanji_list(request, level):
    kanji = Kanji.objects.filter(level=level)
    return render(request, 'kanji_list.html', {'level': level, 'kanji': kanji})

def hiragana(request):
    return render(request, 'hiragana.html')

def katakana(request):
    return render(request, 'katakana.html')

def numbers(request):
    return render(request, 'numbers.html')

@login_required
def progress(request):
    progress = UserProgress.objects.filter(user=request.user)
    return render(request, 'progress.html', {'progress': progress})