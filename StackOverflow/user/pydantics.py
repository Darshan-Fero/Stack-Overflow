import re
from pydantic import BaseModel, validator, ValidationError
from django.contrib.auth.models import User


class RegistrationValidation(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    
    @validator("username", pre=False)
    def is_user_exists(cls, v):
        if len(v) < 4:
            raise ValueError("minimum 4 characters are required")
        if User.objects.filter(username=v).exists():
            raise ValueError("username already exists")
        return v
    
    @validator("password", pre=False)
    def check_password(cls, v):
        if len(v) < 8:
            raise ValueError("minimum 8 characters are required")
        return v
    
    class Config:
        extra = 'forbid'

class CredentialValidation(BaseModel):
    username: str
    password: str
    
    class Config:
        extra = 'forbid'