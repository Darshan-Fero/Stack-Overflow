import re
from QA.models import Answers, Questions
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
        return v
