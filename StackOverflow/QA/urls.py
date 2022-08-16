from locale import T_FMT
from django.urls import path
from .apis import CreateListQuestion, RetrieveQuestion, CreateAnswer, TagsList

urlpatterns = [
    path('question', CreateListQuestion.as_view()),
    path('question/<int:pk>', RetrieveQuestion.as_view()),
    path('answer', CreateAnswer.as_view()),
    path('tags', TagsList.as_view())
]
