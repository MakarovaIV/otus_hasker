from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('signup/', views.register, name="signup"),
    path('login/', views.login_handler, name="login"),
    path('logout/', views.logout_handler, name="logout"),
    path('get_user_image/<int:pk>/', views.get_user_image, name="get_user_image"),
    path('ask/', views.QuestionCreateView.as_view(), name="ask"),
    path('question/<int:question_id>/', views.AnswerQuestionView.as_view(), name="question_detail"),
    path('autocomplete_tag/', views.autocomplete_tag, name="autocomplete_tag"),
    path('answer_vote/', views.answer_votes, name="answer_vote"),
    path('question_vote/', views.question_votes, name="question_vote"),
    path('settings/<int:pk>/', views.UserSettings.as_view(), name="settings"),
    path('user/<int:pk>/', views.UserSettingView.as_view(), name="view_user"),
    path('search_question/', views.search_question, name="search_question"),
    path('answer/', views.answer, name="answer"),
]
