from django.urls import path
from .apis import CreateListQuestion, RetrieveQuestion

urlpatterns = [
    path('question', CreateListQuestion.as_view()),
    path('question/<int:pk>', RetrieveQuestion.as_view())
]
