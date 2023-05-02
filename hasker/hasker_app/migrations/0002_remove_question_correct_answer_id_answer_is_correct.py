# Generated by Django 4.2 on 2023-05-02 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hasker_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='correct_answer_id',
        ),
        migrations.AddField(
            model_name='answer',
            name='is_correct',
            field=models.BooleanField(blank=True, default=False),
        ),
    ]
