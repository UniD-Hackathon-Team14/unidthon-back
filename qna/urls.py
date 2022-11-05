from django.urls import path

from .views import *

urlpatterns = [
    path("category/", CategoryAPI.as_view(), name="question_category_api"),
    path("question/", QuestionAPI.as_view(), name="question_api"),
    path('answer/audio/', AudioAPI.as_view(), name='audio_api'),
    path('answer/image/', ImageAPI.as_view(), name='image_api'),
]
