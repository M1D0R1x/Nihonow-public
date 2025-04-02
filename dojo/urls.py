from django.urls import path
from . import views

urlpatterns = [
    path('', views.dojo_home, name='dojo_home'),
    path('create/', views.create_room, name='create_room'),
    path('join/', views.join_room, name='join_room'),
    path('host/<str:room_code>/', views.host_room, name='host_room'),
    path('participant/<str:room_code>/', views.participant_room, name='participant_room'),
    path('host/<str:room_code>/start/', views.start_competition, name='start_competition'),
    path('host/<str:room_code>/end/', views.end_competition, name='end_competition'),
    path('participant/<str:room_code>/update-score/', views.update_score, name='update_score'),
    path('participant/<str:room_code>/leaderboard/', views.leaderboard, name='leaderboard'),
    path('get_questions/', views.get_questions, name='get_questions'),
]

