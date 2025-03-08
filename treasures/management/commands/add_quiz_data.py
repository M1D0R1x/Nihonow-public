from django.core.management.base import BaseCommand
from treasures.models import QuizQuestion

class Command(BaseCommand):
    help = 'Adds sample quiz questions'

    def handle(self, *args, **kwargs):
        samples = [
            {
                'level': 'N5',
                'question': 'What is こんにちは?',
                'correct_answer': 'hello',
                'wrong_answer1': 'goodbye',
                'wrong_answer2': 'thank you',
                'wrong_answer3': 'sorry',
            },
            {
                'level': 'N5',
                'question': 'What is ありがとう?',
                'correct_answer': 'thank you',
                'wrong_answer1': 'hello',
                'wrong_answer2': 'goodbye',
                'wrong_answer3': 'welcome',
            },
            {
                'level': 'N4',
                'question': 'What is おはよう?',
                'correct_answer': 'good morning',
                'wrong_answer1': 'good night',
                'wrong_answer2': 'hello',
                'wrong_answer3': 'welcome',
            },
            {
                'level': 'N4',
                'question': 'What is さようなら?',
                'correct_answer': 'goodbye',
                'wrong_answer1': 'thank you',
                'wrong_answer2': 'good morning',
                'wrong_answer3': 'welcome',
            },
        ]
        for sample in samples:
            QuizQuestion.objects.update_or_create(
                level=sample['level'],
                question=sample['question'],
                defaults={
                    'correct_answer': sample['correct_answer'],
                    'wrong_answer1': sample['wrong_answer1'],
                    'wrong_answer2': sample['wrong_answer2'],
                    'wrong_answer3': sample['wrong_answer3'],
                }
            )
        self.stdout.write(self.style.SUCCESS('Sample quiz data added or updated!'))