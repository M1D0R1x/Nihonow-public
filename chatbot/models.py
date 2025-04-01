# chatbot/models.py
from django.db import models
from django.contrib.auth.models import User

class ChatLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_logs')
    user_input = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.user.username}: {self.user_input[:30]}..."