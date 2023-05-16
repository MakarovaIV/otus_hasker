from django.urls import path

from api import views

urlpatterns = [
    path('api/v1/', views.QuestionListView.as_view(), name="api_questions_list"),
    path('api/v1/trending/', views.TrendingListView.as_view(), name="api_trending"),
    path('api/v1/question/<int:pk>', views.QuestionDetailView.as_view(), name="api_question_detail"),
    path('api/v1/question/<int:question_id>/answers', views.AnswerView.as_view(), name="api_answers"),
    path('api/v1/question/', views.SearchQuestionView.as_view(), name="api_search_question"),
]

