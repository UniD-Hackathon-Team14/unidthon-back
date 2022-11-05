from django.urls import path

from .views import CategoryAPI, QuestionAPI

urlpatterns = [
    path("category/", CategoryAPI.as_view(), name="question_category_api"),
    path("question/", QuestionAPI.as_view(), name="question_api"),
]
