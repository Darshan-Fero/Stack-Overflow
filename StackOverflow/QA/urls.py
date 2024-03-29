from django.urls import path
from .apis import AcceptAnswer, CreateListQuestion, QuestionRelatedAnswers, RetrieveQuestion, CreateAnswer, RetrieveslugQuestion, TagsList, Votes

urlpatterns = [
    path('<int:question_id>/', QuestionRelatedAnswers.as_view(), name='question-answer-detail'),
    path('question', CreateListQuestion.as_view(), name='question_list'),
    path('question/<int:pk>/', RetrieveQuestion.as_view(), name='question_detail'),
    path('question/<slug:slug>/', RetrieveslugQuestion.as_view(), name='question_slug_detail'),
    path('answers', CreateAnswer.as_view()),
    path('tags', TagsList.as_view()),
    path('vote/<str:qa>/<int:qa_id>', Votes.as_view()),
    path('answer-accept/<int:pk>/', AcceptAnswer.as_view(), name='accept-answer')
]
