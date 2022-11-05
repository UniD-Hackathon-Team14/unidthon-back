from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions
from .models import Category, Question

class CategoryAPI(APIView):
    def get(self, request, **kwargs):
        categories = Category.objects.all()
        return Response(categories)

class QuestionAPI(APIView):
    def get(self, request, **kwargs):
        id = request.GET.get("id")
        if id:
            try:
                question = Question.objects.get(id=id)
                return Response(question)
            except Question.DoesNotExist:
                raise exceptions.ParseError("No question found")

        category = request.GET.get("category")
        if category:
            try:
                question = Question.objects.get(category=category)
                return Response(question)
            except Category.DoesNotExist:
                raise exceptions.ParseError("No question found")

        question = Question.objects.all()
        return Response(question)
