from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import logging
from .bot import get_chatbot_response, api_rate_limiter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('nihonow_views')


def chat_page(request):
    """Render the chat interface page"""
    return render(request, 'chatbot/chat.html')


# Update the view function name to match what's expected in the template
@csrf_exempt
@require_http_methods(["POST"])
def get_response(request):
    """API endpoint for the chatbot"""
    try:
        # Check if the request is JSON
        if request.content_type == 'application/json':
            data = json.loads(request.body)
            user_input = data.get('message', '').strip()
        else:
            user_input = request.POST.get('message', '').strip()

        if not user_input:
            return JsonResponse({'error': 'No message provided'}, status=400)

        # Log the incoming request
        logger.info(f"Received message: {user_input}")

        # Check rate limiting
        if not api_rate_limiter.is_allowed():
            return JsonResponse({
                'response': "I'm receiving too many requests right now. Please try again in a moment."
            })

        # Get response from the chatbot
        response = get_chatbot_response(user_input)

        # Log the response
        logger.info(f"Sending response: {response[:100]}...")

        return JsonResponse({'response': response})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return JsonResponse({'error': 'An error occurred while processing your request'}, status=500)


# Keep the original nihonbot_view as an alias for compatibility
nihonbot_view = get_response

