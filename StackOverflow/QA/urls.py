from django.urls import path
from .apis import CreateListQuestion, QuestionRelatedAnswers, RetrieveQuestion, CreateAnswer, TagsList, Votes

urlpatterns = [
    path('<int:question_id>/', QuestionRelatedAnswers.as_view()),
    path('question', CreateListQuestion.as_view()),
    path('question/<int:pk>/', RetrieveQuestion.as_view()),
    path('answers', CreateAnswer.as_view()),
    path('tags', TagsList.as_view()),
    path('vote/<str:qa>/<int:qa_id>', Votes.as_view()),
]
