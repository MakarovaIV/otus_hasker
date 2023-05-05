from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    picture = models.FileField(upload_to="tmp_upload")
    picture_data = models.BinaryField(blank=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    password1 = models.CharField(max_length=30)
    password2 = models.CharField(max_length=30)

    USERNAME_FIELD = "username"

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.username} ' \
               f'{self.email} ' \
               f'{self.password1} ' \
               f'{self.password2} ' \
               f'{self.picture} ' \
               f'{self.creation_date}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f'{self.pk} {self.name}'


class Question(models.Model):
    title = models.CharField(max_length=300)
    body = models.CharField(blank=True)
    answers_count = models.IntegerField(blank=True, default=0)
    votes_count = models.IntegerField(blank=True, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f'{self.title} ' \
               f'{self.body} ' \
               f'{self.answers_count} ' \
               f'{self.votes_count}' \
               f'{self.creation_date}' \
               f'{self.user}'


class Answer(models.Model):
    body = models.CharField()
    votes_count = models.IntegerField(blank=True, default=0)
    creation_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    is_correct = models.BooleanField(blank=True, default=False)

    def __str__(self):
        return f'{self.body} ' \
               f'{self.votes_count} ' \
               f'{self.creation_date} ' \
               f'{self.user} ' \
               f'{self.is_correct} ' \
               f'{self.question}'


class VoteQuestion(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.user} {self.answer}'


class VoteAnswer(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, default=1)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'{self.user} {self.answer}'
