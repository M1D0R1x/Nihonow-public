# treasures/views.py
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')

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

def contact(request):
    return render(request, 'contact.html')

def resources(request):
    return render(request, 'resources.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})