"""
URL configuration for hasker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from hasker_app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('admin/', admin.site.urls),
    path('signup/', views.register, name="signup"),
    path('login/', views.login_handler, name="login"),
    path('logout/', views.logout_handler, name="logout"),
    path('get_user_image/<int:pk>/', views.get_user_image, name="get_user_image"),
    path('ask/', views.QuestionCreateView.as_view(), name="ask"),
    path('question/<int:question_id>/', views.AnswerQuestionView.as_view(), name="question_detail"),
    path('search_tags/', views.search_tags, name="search_tags"),
    path('answer_vote/', views.answer_votes, name="answer_vote"),
    path('question_vote/', views.question_votes, name="question_vote"),
    path('settings/<int:pk>/', views.UserSettings.as_view(), name="settings"),
    path('user/<int:pk>/', views.UserSettingView.as_view(), name="view_user"),
    path('search_question/', views.search_question, name="search_question"),
    path('answer_question/', views.answer_question, name="answer_question"),
]
