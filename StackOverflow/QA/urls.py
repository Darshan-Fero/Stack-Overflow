from django.urls import path
from .apis import CreateQuestion

urlpatterns = [
    path('question', CreateQuestion.as_view())
]
