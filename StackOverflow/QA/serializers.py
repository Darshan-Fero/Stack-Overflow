from rest_framework.serializers import ModelSerializer, ValidationError, SerializerMethodField
from user.utils import pydantic_validation
from .models import Questions, Tags
from .pydantics import QuestionValidation


class CreateQuestionSerializer(ModelSerializer):
    
    tag = SerializerMethodField()    
    class Meta:
        model = Questions
        fields = (
            'author',
            'title',
            'body',
            'tag',
        )
    def to_internal_value(self, data):
        return data
        
    def validate(self, data):
        is_valid, msg = pydantic_validation(QuestionValidation, data)
        if not is_valid:
            raise ValidationError({'message':msg})
        data.update({'tag':Tags.objects.get(name=data['tag'])})
        return data
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.update({'author':request.user})
        question = Questions(**validated_data)
        question.save()
        return question
    
    def get_tag(self, obj):
        return obj.tag.name
        
        
class ListQuestionSerializer(ModelSerializer):
    
    tag = SerializerMethodField()
    class Meta:
        model = Questions
        fields = "__all__"
        
    def get_tag(self, obj):
        return obj.tag.name