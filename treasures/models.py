from django.db import models
from django.contrib.auth.models import User

class Vocabulary(models.Model):
    LEVEL_CHOICES = [
        ('N5', 'N5'),
        ('N4', 'N4'),
        ('N3', 'N3'),
        ('N2', 'N2'),
        ('N1', 'N1'),
    ]
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    word = models.CharField(max_length=50)
    reading = models.CharField(max_length=50)
    meaning = models.CharField(max_length=100)
    example = models.TextField(blank=True)
    audio = models.FileField(upload_to='audio/', blank=True)

    def __str__(self):
        return f"{self.word} ({self.level})"

class QuizQuestion(models.Model):
    level = models.CharField(max_length=2, choices=Vocabulary.LEVEL_CHOICES)
    question = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)
    wrong_answer1 = models.CharField(max_length=100)
    wrong_answer2 = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.question} ({self.level})"

class Kanji(models.Model):
    level = models.CharField(max_length=2, choices=Vocabulary.LEVEL_CHOICES)
    character = models.CharField(max_length=1)
    on_reading = models.CharField(max_length=50, blank=True)
    kun_reading = models.CharField(max_length=50, blank=True)
    meaning = models.CharField(max_length=100)
    stroke_count = models.IntegerField()

    def __str__(self):
        return f"{self.character} ({self.level})"

class UserProgress(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    level = models.CharField(max_length=2, choices=Vocabulary.LEVEL_CHOICES)
    studied = models.BooleanField(default=False)
    quiz_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.level}"