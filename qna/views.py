import random

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions

from account.models import User
from .models import Category, Question, Diary, Answer
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
                question_queryset = Question.objects.filter(category__title=category, type=type)
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
                        question_result |= Question.objects.filter(pk=question_queryset[question_id].pk)
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
        user = request.user.pk
        data['user'] = user
        data['type'] = 'audio'
        serializer = DiarySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(dict(result='Success'))
        else:
            raise exceptions.ParseError("Not Created")

class ImageAPI(APIView):
    def post(self, request):
        user = request.user
        answer_list = request.data['answers']
        for answer in answer_list:
            Diary.objects.create(user=user,
                                 type='image',
                                 answer=Answer.objects.get(pk=answer))
        return Response(dict(result='Success'))

class HistoryAPI(APIView):
    @csrf_exempt
    def get(self, request):
        user = User.objects.get(pk=1)
        category = request.GET.get("category")
        type = request.GET.get("type")
        # 카테고리가 있는 경우
        if (category):
            if (type == 'audio'):
                diary_queryset = user.diary.filter(type=type, question__category__title=category)
            else:
                diary_queryset = user.diary.filter(type=type, answer__question__category__title=category)
        else :
            diary_queryset = user.diary.filter(type=type)

        # 음성인 경우 바로 리스트를 바로 return
        if (type == 'audio'):
            audio_list = []
            for diary in diary_queryset:
                audio_list.append(dict(question=diary.question.contents,
                                       audio=diary.audio_dirs.url,
                                       created_at=diary.created_at))
            return Response(dict(nickname=user.nickname,
                                 audio_list=audio_list))

        if (type == 'image'):
            image_list = {}
            for diary in diary_queryset:
                date = diary.created_at.strftime("%Y-%m-%d")
                category = diary.answer.question.category.title
                date_category = str(date) + '/' + str(category)
                image_data = dict(question=diary.answer.question.contents,
                                  image=diary.answer.image_dirs.url)
                try:
                    image_list[date_category] = image_list[date_category] + [image_data]
                    # print(image_list[date_category])
                except:
                    image_list[date_category] = [image_data]
                    # print(image_list[date_category])
            image_result = []
            image_list = dict(sorted(image_list.items()))
            for k, v in image_list.items():
                s = k.split('/')
                image_result.append(dict(date=s[0],
                                         category=s[1],
                                         image_list=v))
            return Response(image_result)



