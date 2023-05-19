from django.urls import path, include

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api import views

schema_view = get_schema_view(
   openapi.Info(
      title="Hasker API",
      default_version='v1',
      description="API for questions from hasker service",
      contact=openapi.Contact(email="test@mail.ru"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('api/v1/', views.QuestionListView.as_view(), name="api_questions_list"),
    path('api/v1/trending/', views.TrendingListView.as_view(), name="api_trending"),
    path('api/v1/question/<int:pk>/', views.QuestionDetailView.as_view(), name="api_question_detail"),
    path('api/v1/question/<int:question_id>/answers/', views.AnswerView.as_view(), name="api_answers"),
    path('api/v1/question/', views.SearchQuestionView.as_view(), name="api_search_question"),
    path("api/v1/swagger/", schema_view.with_ui('swagger', cache_timeout=0)),
    path("api/v1/redoc/", schema_view.with_ui('redoc', cache_timeout=0)),
    path("api-auth/", include('rest_framework.urls', namespace='rest_framework'))
]
