from django import template
from django.utils.timezone import now

register = template.Library()

@register.simple_tag
def get_greeting(username):
    current_hour = now().hour
    if current_hour < 12:
        return f"Ohayo Gozaimasu {username}!"
    elif current_hour < 18:
        return f"Konnichiwa {username}!"
    else:
        return f"Konbanwa {username}!"