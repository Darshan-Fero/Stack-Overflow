import re
from QA.models import Answers, Questions, Tags
from pydantic import BaseModel, validator, ValidationError
from django.contrib.auth.models import User
from enum import Enum


class QuestionValidation(BaseModel):
    title: str
    body: str
    tag: str
    
    @validator("title", pre=False)
    def check_title(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        return v

    @validator("body", pre=False)
    def check_body(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        return v

    @validator("tag", pre=False)
    def check_tag(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        v = Tags.objects.filter(name=v).first()
        if not v:
            raise ValueError("Invalid Tag")
        return v

class AnswerValidation(BaseModel):
    question_id: int
    body: str
    
    @validator("question_id", pre=False)
    def check_question_id(cls, v):
        if type(v)!=int and not str(v).isdecimal():
            return ValueError("Invalid question id")
        if not Questions.objects.filter(id=int(v)):
            return ValueError("Invalid question id")
        return v

    @validator("body", pre=False)
    def check_body(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        return v

class TagValidation(BaseModel):
    name: str

    @validator("name", pre=False)
    def check_name(cls, v):
        if not v:
            raise ValueError("Blank not allowed")
        return v