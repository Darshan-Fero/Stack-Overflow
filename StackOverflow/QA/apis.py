from rest_framework.generics import RetrieveAPIView, ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Questions, Tags
from .serializers import CreateQuestionSerializer, ListQuestionSerializer, CreateAnswerSerializer, QuestionRelatedAnswersSerializer, TagsSerializer, VoteToQuestionSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.authentication import TokenAuthentication
from django.http import HttpResponseNotFound

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
    
    def get_queryset(self):
        tag = self.request.GET.get('tag')
        author_id = self.request.GET.get('author_id')
        queryset = self.queryset
        if str(author_id).isdecimal():
            author = User.objects.filter(pk=int(author_id)).first()
            queryset = queryset.filter(author=author)
        if tag:
            tag = Tags.objects.filter(name__iexact=tag).first()
            queryset = queryset.filter(tags=tag)
        return queryset
    
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
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
    
    
class Votes(APIView):
    '''
    API to give Vote to questions and answer
    '''
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, qa, qa_id, *args, **kwargs):
        if qa not in ['question', 'answer']:
            return HttpResponseNotFound()
        data = request.data
        data.update({qa:qa_id})
        serializer = VoteToQuestionSerializer(data=data, context={'request':request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(data={})