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

    class Meta:
        verbose_name_plural = "카테고리"

    def __str__(self):
        return self.title

class Question(models.Model):
    category = models.ForeignKey(Category, verbose_name='카테고리', on_delete=models.CASCADE, related_name="question")
    type = models.CharField('타입', max_length=32, choices=AnswerType.TYPE.value,
                              default=AnswerType.IMAGE.value)
    contents = models.TextField('질문')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "질문"

    def __str__(self):
        return self.contents

class Answer(models.Model):
    question = models.ForeignKey(Question, verbose_name='질문', on_delete=models.CASCADE, related_name="answer")
    image_dirs = models.ImageField(upload_to=uuid_name, blank=True, null=True)

    class Meta:
        verbose_name_plural = "응답"

    def __str__(self):
        return self.question

class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='질문', on_delete=models.CASCADE, related_name="diary")
    type = models.CharField('타입', max_length=32, choices=AnswerType.TYPE.value,
                              default=AnswerType.IMAGE.value)
    answer = models.ForeignKey(Answer, verbose_name='응답', on_delete=models.CASCADE, related_name="diary")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "다이어리"

    def __str__(self):
        return self.user + self.type