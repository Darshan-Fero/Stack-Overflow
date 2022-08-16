from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView, ListAPIView
from rest_framework.response import Response
from .models import Questions, Tags
from .serializers import CreateQuestionSerializer, ListQuestionSerializer, CreateAnswerSerializer, QuestionRelatedAnswersSerializer, TagsSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authentication import TokenAuthentication

class BaseLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100

class CreateListQuestion(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Questions.objects.all()
    pagination_class = BaseLimitOffsetPagination
    
    def get_serializer_class(self, *args):
        if self.request.method == 'POST':
            return CreateQuestionSerializer
        return ListQuestionSerializer
    
class RetrieveQuestion(RetrieveUpdateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except ValueError as e:
            return Response({'message':str(e)}, status=400)

    def put(self, request, *args, **kwargs):
        try:
            return self.update(request, *args, **kwargs)
        except ValueError as e:
            return Response({'message':str(e)}, status=400)

    def get_serializer_class(self, *args):
        if self.request.method == 'PUT':
            return CreateQuestionSerializer
        return ListQuestionSerializer
    
    def get_object(self):
        question_id = self.kwargs[self.lookup_field]
        instance = Questions.objects.filter(pk=question_id).first()
        if not instance:
            raise ValueError('Invalid question id')
        return instance

    
class CreateAnswer(CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateAnswerSerializer


class TagsPagination(LimitOffsetPagination):
    default_limit = 50
    max_limit = 200

class TagsList(ListCreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = TagsSerializer
    pagination_class = TagsPagination
    queryset = Tags.objects.all()
    
    
class QuestionRelatedAnswers(RetrieveAPIView):
    serializer_class = QuestionRelatedAnswersSerializer
    lookup_field = 'question_id'
    
    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except ValueError as e:
            return Response({'message':str(e)}, status=400)
        
    def get_object(self):
        question_id = self.kwargs[self.lookup_field]
        instance = Questions.objects.filter(pk=question_id).first()
        if not instance:
            raise ValueError('Invalid question id')
        return instance