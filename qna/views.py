import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions

from .models import Category, Question
from .serializers import DiarySerializer


class CategoryAPI(APIView):
    def get(self, request, **kwargs):
        categories_list = Category.objects.values('pk', 'title', 'description')
        return Response(categories_list)

class QuestionAPI(APIView):
    def get(self, request, **kwargs):
        category = request.GET.get("category")
        type = request.GET.get("type")
        if category:
            try:
                question_queryset = Question.objects.filter(category__pk=category, type=type)
                # user 가 있는 경우 필터링
            except Question.DoesNotExist:
                raise exceptions.ParseError("No question found")
        # 음성인 경우 질문 1개 추출, 이미지인 경우 3개 추출
        if question_queryset.count():
            if (type == 'audio'):
                random_num = random.randrange(0, len(question_queryset))
                question_object = question_queryset[random_num]
                return Response(dict(question=question_object.pk,
                                     contents=question_object.contents))
            if (type == 'image'):
                if (question_queryset.count() > 3):
                    question_list = random.sample(range(question_queryset.count()), 3)
                    question_result = Question.objects.none()
                    for question_id in question_list:
                        question_result |= Question.objects.filter(pk=question_id)
                    question_queryset = question_result
                question_list = []
                for question in question_queryset:
                    answer_list = question.answer.all()
                    answer_image_list = []
                    for answer_list in answer_list:
                        answer_image_list.append(answer_list.image_dirs.url)
                    question_list.append(dict(question=question.pk,
                                              contents=question.contents,
                                              answer_list=answer_image_list))
                return Response(question_list)

        else:
            raise exceptions.ParseError("All question answered")


class AudioAPI(APIView):
    def post(self, request):
        data = request.data
        data['type'] = 'audio'
        serializer = DiarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(dict(result='Success'))
        else:
            raise exceptions.ParseError("Not Created")