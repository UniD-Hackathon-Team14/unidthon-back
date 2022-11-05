import os
import uuid

from django.db import models
from django.utils import timezone
from django.conf import settings

from unidthon_back.data.enum import AnswerType


def uuid_name(instance, filename):
    name = uuid.uuid4()
    extension = os.path.splitext(filename)[-1].lower()
    return '/'.join([
        'media',
        'answer',
        str(name)+extension,
    ])

class Category(models.Model):
    title = models.CharField('카테고리', max_length=10)
    description = models.TextField('설명', blank=True)

class Question(models.Model):
    category = models.ForeignKey(Category, verbose_name='카테고리', on_delete=models.CASCADE)
    contents = models.TextField('질문')
    created_at = models.DateTimeField(default=timezone.now)

class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='질문', on_delete=models.CASCADE)
    image_dirs = models.ImageField(upload_to=uuid_name, blank=True, null=True)

class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='질문', on_delete=models.CASCADE)
    type = models.CharField('타입', max_length=32, choices=AnswerType.TYPE.value,
                              default=AnswerType.IMAGE.value)
    answer = models.ForeignKey(Answer, verbose_name='응답', on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)