from rest_framework.response import Response
from rest_framework.views import APIView
from .pydantics import CredentialValidation, RegistrationValidation
from .utils import generate_token, pydantic_validation
from django.contrib.auth.models import User
from django.contrib import auth


class RegistrationAPIView(APIView):
    '''
    Registration of new User and retun a token
    '''
    
    def post(self, request, *args, **kwargs):
        data = request.data

        is_valid, msg = pydantic_validation(RegistrationValidation, data)
        if not is_valid:
            return Response(msg, status=400)

        password = data.pop('password')
        user = User(**data)
        user.set_password(password)
        user.save()
        
        token = generate_token(user)
        return Response({'token':token}, status=201)
    
class SinginAPIView(APIView):
    '''
    Singin and return a token
    '''

    def post(self, request, *args, **kwargs):
        data = request.data
        
        is_valid, msg = pydantic_validation(CredentialValidation, data)
        if not is_valid:
            return Response(msg, status=400)

        user = auth.authenticate(username=data.get('username'), password=data.get('password'))
        if not user:
            return Response("Wrong username or password", 401)

        token = generate_token(user)
        return Response({'token':token})