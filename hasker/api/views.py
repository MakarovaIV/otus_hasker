from rest_framework import generics, filters

from . import serializers
import environ

from hasker_app.models import Question, Answer, Tag


env = environ.Env()
environ.Env.read_env()


class SignUpView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer


class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    paginate_by = env('INDEX_PAGINATION')


class TrendingListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    paginate_by = env('TRENDING_PAGINATION')
    queryset = Question.objects.all().order_by('-votes_count', '-creation_date')[:int(env('TRENDING_PAGINATION'))]


class QuestionDetailView(generics.RetrieveAPIView):
    queryset = Question.objects.all()
    serializer_class = serializers.QuestionSerializer
    lookup_field = 'pk'


class AnswerView(generics.ListAPIView):
    serializer_class = serializers.AnswerSerializer
    lookup_field = 'question_id'

    def get_queryset(self):
        queryset = Answer.objects.filter(question_id=self.kwargs['question_id']).order_by('-votes_count', '-creation_date')
        return queryset


class SearchQuestionView(generics.ListAPIView):
    serializer_class = serializers.QuestionSerializer
    search_fields = ['title', 'tags__name']
    filter_backends = (filters.SearchFilter,)
    queryset = Question.objects.all()
