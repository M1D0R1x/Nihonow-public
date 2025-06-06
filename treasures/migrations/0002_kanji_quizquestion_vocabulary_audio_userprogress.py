# Generated by Django 5.1.7 on 2025-03-07 12:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('treasures', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kanji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('N5', 'N5'), ('N4', 'N4'), ('N3', 'N3'), ('N2', 'N2'), ('N1', 'N1')], max_length=2)),
                ('character', models.CharField(max_length=1)),
                ('on_reading', models.CharField(blank=True, max_length=50)),
                ('kun_reading', models.CharField(blank=True, max_length=50)),
                ('meaning', models.CharField(max_length=100)),
                ('stroke_count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='QuizQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('N5', 'N5'), ('N4', 'N4'), ('N3', 'N3'), ('N2', 'N2'), ('N1', 'N1')], max_length=2)),
                ('question', models.CharField(max_length=100)),
                ('correct_answer', models.CharField(max_length=100)),
                ('wrong_answer1', models.CharField(max_length=100)),
                ('wrong_answer2', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='vocabulary',
            name='audio',
            field=models.FileField(blank=True, upload_to='audio/'),
        ),
        migrations.CreateModel(
            name='UserProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(choices=[('N5', 'N5'), ('N4', 'N4'), ('N3', 'N3'), ('N2', 'N2'), ('N1', 'N1')], max_length=2)),
                ('studied', models.BooleanField(default=False)),
                ('quiz_completed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
