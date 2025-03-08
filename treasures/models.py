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
    level = models.CharField(max_length=2, choices=[('N5', 'N5'), ('N4', 'N4'), ('N3', 'N3'), ('N2', 'N2'), ('N1', 'N1')])
    question = models.CharField(max_length=255)
    wrong_answer1 = models.CharField(max_length=100)  # Reverted from option1
    wrong_answer2 = models.CharField(max_length=100)  # Reverted from option2
    wrong_answer3 = models.CharField(max_length=100)  # Reverted from option3
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.level} - {self.question}"

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.CharField(max_length=2, choices=[('N5', 'N5'), ('N4', 'N4'), ('N3', 'N3'), ('N2', 'N2'), ('N1', 'N1')])
    lessons_completed = models.IntegerField(default=0)
    total_lessons = models.IntegerField(default=10)  # Example: 10 lessons per level
    quiz_score = models.FloatField(default=0.0)
    updated_at = models.DateTimeField(auto_now=True)

    def progress_percentage(self):
        return (self.lessons_completed / self.total_lessons) * 100

    def __str__(self):
        return f"{self.user.username} - {self.level}"

class DailyWord(models.Model):
    date = models.DateField(unique=True)
    reading = models.CharField(max_length=100)  # Reverted to original name
    word = models.CharField(max_length=100)     # Reverted to original name
    english_meaning = models.CharField(max_length=200, default="No meaning available")  # Added with default

    def __str__(self):
        return f"{self.reading} ({self.word}) - {self.english_meaning}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

class Tip(models.Model):
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[:50]