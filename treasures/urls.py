from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('numbers/', views.numbers, name='numbers'),
    path('hiragana/', views.hiragana, name='hiragana'),
    path('katakana/', views.katakana, name='katakana'),
    path('n5/', views.n5, name='n5'),
    path('n5/quiz/', views.n5_quiz, name='n5_quiz'),
    path('n5/kanji/', views.n5_kanji, name='n5_kanji'),
    path('n4/', views.n4, name='n4'),
    path('n4/quiz/', views.n4_quiz, name='n4_quiz'),
    path('n4/kanji/', views.n4_kanji, name='n4_kanji'),
    path('n3/', views.n3, name='n3'),
    path('n3/quiz/', views.n3_quiz, name='n3_quiz'),
    path('n3/kanji/', views.n3_kanji, name='n3_kanji'),
    path('n2/', views.n2, name='n2'),
    path('n2/quiz/', views.n2_quiz, name='n2_quiz'),
    path('n2/kanji/', views.n2_kanji, name='n2_kanji'),
    path('n1/', views.n1, name='n1'),
    path('n1/quiz/', views.n1_quiz, name='n1_quiz'),
    path('n1/kanji/', views.n1_kanji, name='n1_kanji'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    # New URL patterns added below
    path('about/', views.about, name='about'),
    path('resources/', views.resources, name='resources'),
    path('contact/', views.contact, name='contact'),
]