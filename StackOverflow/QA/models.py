from time import timezone
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify


# Create your models here.

class TimeStampsModel(models.Model):
    
    created = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Tags(models.Model):
    
    name = models.CharField(null=True, blank=True, max_length=100, unique=True)
    
    class Meta:
        app_label = 'QA'
        verbose_name = 'Tags'
        verbose_name_plural = 'Tags'
        
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        is_exists = Tags.objects.filter(name__iexact=self.name)
        if is_exists:
            raise ValueError(str(self.name)+' tag already exists')
        super(Tags, self).save(*args, **kwargs)


class Questions(TimeStampsModel):
    
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tags, related_name='questions_by_tag', related_query_name='questions_by_tag')
    vote = models.IntegerField(default=0)
    slug = models.SlugField(null=True, blank=True, unique=True)
    
    class Meta:
        app_label = 'QA'
        verbose_name = 'Questions'
        verbose_name_plural = 'Questions'
        
    def save(self, *args, **kwargs):  # new
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"pk": self.slug})
        
    def __str__(self):
        return str(self.title)+'-'+str(self.id)


class Answers(TimeStampsModel):
    
    author = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    body = models.TextField(null=True, blank=True)
    vote = models.IntegerField(default=0)
    is_approved = models.BooleanField(default=False)
    
    class Meta:
        app_label = 'QA'
        verbose_name = 'Answers'
        verbose_name_plural = 'Answers'
        
    def __str__(self):
        return str(self.question.title)+'-'+str(self.id)
    
VOTE_CHOICES = (
        ('', '-----'),
        ('UP', 'UP'),
        ('DOWN', 'DOWN')
    )

class QuestionsVote(models.Model):
    
    question = models.ForeignKey(Questions, related_name='votes', related_query_name='votes', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    vote = models.CharField(max_length=50, choices=VOTE_CHOICES)

    class Meta:
        app_label = 'QA'
        verbose_name = "Question's Votes"
        verbose_name_plural = "Question's Votes"
        unique_together = ('question', 'user',)
        
    def save(self, *args, **kwargs):
        super(QuestionsVote, self).save(*args, **kwargs)
        question = Questions.objects.get(pk=self.question.id)
        up = len(QuestionsVote.objects.filter(vote='UP'))
        down = len(QuestionsVote.objects.filter(vote='DOWN'))
        question.vote = up-down
        question.save()
        
        
    def __str__(self):
        return 'Question - '+str(self.question.title)+' - '+str(self.vote)


class AnswersVote(models.Model):
    
    answer = models.ForeignKey(Answers, related_name='votes', related_query_name='votes', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    vote = models.CharField(max_length=50, choices=VOTE_CHOICES)

    class Meta:
        app_label = 'QA'
        verbose_name = "Answer's Votes"
        verbose_name_plural = "Answer's Votes"
        unique_together = ('answer', 'user',)

    def save(self, *args, **kwargs):
        super(AnswersVote, self).save(*args, **kwargs)
        answer = Answers.objects.get(pk=self.answer.id)
        up = len(AnswersVote.objects.filter(vote='UP'))
        down = len(AnswersVote.objects.filter(vote='DOWN'))
        answer.vote = up-down
        answer.save()
        
    def __str__(self):
        return 'Answer - '+str(self.answer.question.title)+' - '+str(self.vote)
