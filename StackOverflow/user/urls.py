from django.urls import path
from .apis import RegistrationAPIView, SinginAPIView


urlpatterns = [
    path('signup', RegistrationAPIView.as_view(), name='signup'),
    path('signin', SinginAPIView.as_view(), name='signin'),
]