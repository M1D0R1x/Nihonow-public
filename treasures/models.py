from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    email_confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

    def save(self, *args, **kwargs):
        # Sync email_confirmed with user.is_active
        if self.email_confirmed and not self.user.is_active:
            self.user.is_active = True
            self.user.save()
        elif not self.email_confirmed and self.user.is_active:
            self.user.is_active = False
            self.user.save()
        super().save(*args, **kwargs)

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
    reading = models.CharField(max_length=100)
    word = models.CharField(max_length=100)
    english_meaning = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.reading} ({self.word}) - {self.english_meaning}"

class Kanji(models.Model):
    level = models.CharField(max_length=2, choices=[
        ('N5', 'N5'),
        ('N4', 'N4'),
        ('N3', 'N3'),
        ('N2', 'N2'),
        ('N1', 'N1'),
    ])
    character = models.CharField(max_length=1)
    on_reading = models.CharField(max_length=50, blank=True)
    kun_reading = models.CharField(max_length=50, blank=True)
    meaning = models.CharField(max_length=100)
    stroke_count = models.IntegerField()

    def __str__(self):
        return f"{self.character} ({self.level})"

class DailyKanji(models.Model):
    date = models.DateField(unique=True)
    kanji = models.ForeignKey(Kanji, on_delete=models.CASCADE, related_name='daily_kanji')
    example_sentence = models.CharField(max_length=200, blank=True)
    example_translation = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Kanji of the Day for {self.date}: {self.kanji.character}"

class QuizQuestion(models.Model):
    level = models.CharField(max_length=2, choices=[('N5', 'N5'), ('N4', 'N4'), ('N3', 'N3'), ('N2', 'N2'), ('N1', 'N1')])
    question = models.CharField(max_length=255)
    wrong_answer1 = models.CharField(max_length=100)
    wrong_answer2 = models.CharField(max_length=100)
    wrong_answer3 = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.level} - {self.question}"