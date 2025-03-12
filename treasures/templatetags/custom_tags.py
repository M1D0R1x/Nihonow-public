from django import template
from django.utils.timezone import now
import pytz

register = template.Library()


@register.simple_tag
def get_greeting(username):
    # Explicitly use the TIME_ZONE from settings
    from django.conf import settings
    tz = pytz.timezone(settings.TIME_ZONE)  # Should be 'Asia/Kolkata'
    current_time = now().astimezone(tz)
    current_hour = current_time.hour

    if current_hour < 12:
        return f"Ohayo Gozaimasu {username}!"
    elif current_hour < 18:
        return f"Konnichiwa {username}!"
    else:
        return f"Konbanwa {username}!"