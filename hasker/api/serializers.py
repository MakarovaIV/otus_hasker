from rest_framework import serializers
from hasker_app.models import CustomUser, Question, Answer, Tag


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name')


class QuestionSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    tags = TagSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'user', 'title', 'body', 'tags']


class AnswerSerializer(serializers.ModelSerializer):
    asked_user = serializers.ReadOnlyField(source='user.username')
    question_title = serializers.ReadOnlyField(source='question.title')
    question_body = serializers.ReadOnlyField(source='question.body')

    class Meta:
        model = Answer
        fields = ['id', 'question_title', 'question_body', 'asked_user', 'body']
