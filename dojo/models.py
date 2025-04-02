from django.db import models
from django.contrib.auth.models import User
import random
import string


def generate_room_code():
    """Generate a random 6-digit code for the room"""
    return ''.join(random.choices(string.digits, k=6))


class DojoRoom(models.Model):
    code = models.CharField(max_length=6, unique=True, default=generate_room_code)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hosted_rooms')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    has_started = models.BooleanField(default=False)
    has_ended = models.BooleanField(default=False)

    # Room settings
    category = models.CharField(max_length=20, null=True, blank=True)
    subcategory = models.CharField(max_length=20, null=True, blank=True)
    question_type = models.CharField(max_length=10, null=True, blank=True)
    time_limit = models.IntegerField(default=60)

    def __str__(self):
        return f"{self.name} ({self.code})"


class DojoParticipant(models.Model):
    room = models.ForeignKey(DojoRoom, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dojo_participations')
    score = models.IntegerField(default=0)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f"{self.user.username} in {self.room.code}"

