from time import timezone
from xml.dom import ValidationErr
from django.db import models
from django.contrib.auth.models import User

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
    
    class Meta:
        app_label = 'QA'
        verbose_name = 'Questions'
        verbose_name_plural = 'Questions'
        
    def __str__(self):
        return str(self.title)


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
        return str(self.question.title)

    
    