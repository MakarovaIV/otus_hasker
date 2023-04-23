from django.db import models
from django.contrib.auth.models import AbstractUser

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    picture = models.FileField(upload_to="tmp_upload")
    picture_data = models.BinaryField(null=True)
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


class Question(models.Model):
    title = models.CharField(max_length=300, unique=True)
    body = models.CharField()
    answers_count = models.IntegerField()
    votes_count = models.IntegerField()
    creation_date = models.DateTimeField()
    correct_answer_id = models.BooleanField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} ' \
               f'{self.body} ' \
               f'{self.answers_count} ' \
               f'{self.votes_count}' \
               f'{self.creation_date}' \
               f'{self.correct_answer_id}' \
               f'{self.user_id}'


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    tag_id = models.ManyToManyField(Question)

    def __str__(self):
        return f'{self.tag_id} {self.name}'


class Answer(models.Model):
    body = models.CharField()
    votes_count = models.IntegerField()
    creation_date = models.DateTimeField()
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.body} ' \
               f'{self.votes_count} ' \
               f'{self.creation_date} ' \
               f'{self.user_id} ' \
               f'{self.question_id}'


class VoteQuestion(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    question_id = models.OneToOneField(Question, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f'{self.user_id} {self.question_id}'


class VoteAnswer(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    answer_id = models.OneToOneField(Answer, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return f'{self.user_id} {self.answer_id}'
