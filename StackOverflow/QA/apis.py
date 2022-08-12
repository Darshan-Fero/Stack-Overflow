from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Questions
from .serializers import CreateQuestionSerializer, ListQuestionSerializer
from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import LimitOffsetPagination

class BaseLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 20
    max_limit = 100

class CreateListQuestion(ListCreateAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Questions.objects.all()
    pagination_class = BaseLimitOffsetPagination

    def create(self, request, *args, **kwargs):
        serialize = self.get_serializer(data=request.data, context={'request':request})
        if not serialize.is_valid():
            return Response(data=serialize.errors.get('non_field_errors'), status=400)
        serialize.save()
        return Response(data={}, status=201)
    
    def get_serializer_class(self, *args):
        if self.request.method == 'POST':
            return CreateQuestionSerializer
        return ListQuestionSerializer
    
class RetrieveQuestion(RetrieveAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ListQuestionSerializer
    
    def get_object(self):
        question_id = self.kwargs[self.lookup_field]
        instance = Questions.objects.filter(pk=question_id).first()
        if not instance:
            raise ValueError('Invalid question id')
        return instance
    
    def get(self, request, *args, **kwargs):
        try:
            return self.retrieve(request, *args, **kwargs)
        except ValueError as e:
            return Response({'message':str(e)}, status=400)
    
    
    
    