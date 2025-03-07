from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('level/<str:level>/', views.level_detail, name='level_detail'),
    path('quiz/<str:level>/', views.quiz, name='quiz'),
    path('kanji/<str:level>/', views.kanji_list, name='kanji_list'),
    path('hiragana/', views.hiragana, name='hiragana'),
    path('katakana/', views.katakana, name='katakana'),
    path('numbers/', views.numbers, name='numbers'),
    path('progress/', views.progress, name='progress'),  # New URL for progress
]