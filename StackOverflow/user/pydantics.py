from pydantic import BaseModel, validator
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class RegistrationValidation(BaseModel):
    email: str
    username: str
    password: str
    first_name: str
    last_name: str
    
    @validator("email", pre=False)
    def check_email(cls, v):
        if User.objects.filter(email=v).exists():
            raise ValueError("email already exists")
        try:
            validate_email(v)
        except ValidationError:
            raise ValueError("Invalid email")
        return v

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