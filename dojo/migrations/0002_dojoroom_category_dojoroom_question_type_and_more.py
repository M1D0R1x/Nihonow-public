# Generated by Django 5.1.7 on 2025-04-02 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dojoroom',
            name='category',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='dojoroom',
            name='question_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='dojoroom',
            name='subcategory',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='dojoroom',
            name='time_limit',
            field=models.IntegerField(default=60),
        ),
    ]
