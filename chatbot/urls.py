from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('nihonbot/', views.nihonbot_view, name='nihonbot'),
    path('get_response/', views.get_response, name='get_response'),  # Add this line
]

