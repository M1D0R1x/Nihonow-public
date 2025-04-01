from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('get_response/', views.nihonbot_view, name='get_response'),
    path('history/', views.nihonbot_view, name='chat_history'),  # Same view handles both POST and GET
]

