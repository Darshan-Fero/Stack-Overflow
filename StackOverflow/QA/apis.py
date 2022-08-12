from rest_framework.generics import ListCreateAPIView
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

class CreateQuestion(ListCreateAPIView):
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
    