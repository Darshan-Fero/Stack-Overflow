from rest_framework.serializers import ModelSerializer, ValidationError
from user.utils import pydantic_validation
from .models import Questions
from .pydantics import QuestionValidation


class CreateQuestionSerializer(ModelSerializer):
    
    class Meta:
        model = Questions
        fields = (
            'author',
            'title',
            'body',
            'tag',
        )
        
    def validate(self, data):
        is_valid, msg = pydantic_validation(QuestionValidation, data)
        if not is_valid:
            raise ValidationError(msg)
        return data
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.update({'author':request.user})
        question = Questions(**validated_data)
        question.save()
        return question
        
        
class ListQuestionSerializer(ModelSerializer):
    
    class Meta:
        model = Questions
        fields = "__all__"