from django.shortcuts import render
from django.http import JsonResponse
from .bot import get_chatbot_response
from .models import ChatLog

def chat_page(request):
    return render(request, 'chatbot/chat.html')  # Path resolves to templates/chatbot/

def get_response(request):
    if request.method == 'POST':
        user_input = request.POST.get('message', '').strip()
        if not user_input:
            return JsonResponse({'error': 'No message provided'}, status=400)
        response = get_chatbot_response(user_input)
        ChatLog.objects.create(user_input=user_input, bot_response=response)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)