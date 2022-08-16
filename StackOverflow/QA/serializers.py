import zoneinfo
from rest_framework.serializers import Serializer, ModelSerializer, ValidationError, SerializerMethodField, HyperlinkedModelSerializer
from user.utils import pydantic_validation
from .models import Answers, Questions, Tags
from .pydantics import QuestionValidation, AnswerValidation, TagValidation
from .tasks import sendEmail


class CreateQuestionSerializer(ModelSerializer):
    
    tag = SerializerMethodField()    
    class Meta:
        model = Questions
        fields = (
            'id',
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
        return data
        
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.update({'tag':Tags.objects.get(name=validated_data['tag'])})
        validated_data.update({'author':request.user})
        question = Questions(**validated_data)
        question.save()
        return question
    
    def get_tag(self, obj):
        return obj.tag.name


class ListQuestionSerializer(ModelSerializer):
    
    tag = SerializerMethodField()
    created = SerializerMethodField()
    updated = SerializerMethodField()
    class Meta:
        model = Questions
        fields = ('id', 'author', 'title', 'body', 'tag', 'vote', 'created', 'updated')
        
    def get_tag(self, obj):
        return obj.tag.name
    
    def get_created(self, obj):
        indian_tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        datetime = {
            "date":obj.updated.astimezone(indian_tz).strftime("%Y-%m-%d"),
            "time":obj.updated.astimezone(indian_tz).strftime("%H:%M")
        }
        return datetime

    def get_updated(self, obj):
        indian_tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        datetime = {
            "date":obj.updated.astimezone(indian_tz).strftime("%Y-%m-%d"),
            "time":obj.updated.astimezone(indian_tz).strftime("%H:%M")
        }
        return datetime
    
    
class CreateAnswerSerializer(ModelSerializer):
    
    class Meta:
        model = Answers
        fields = (
            'question_id',
            'body',
            'author',
        )
        
    def to_internal_value(self, data):
        return data
        
    def validate(self, data):
        is_valid, msg = pydantic_validation(AnswerValidation, data)
        if not is_valid:
            raise ValidationError({'message':msg})
        return data
    
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data.update({'question':Questions.objects.get(id=int(validated_data['question_id']))})
        validated_data.update({'author':request.user})
        answer = Answers(**validated_data)
        answer.save()
        sender = "info@StackOverflow.com"
        receiver = answer.question.author.email
        sendEmail.delay(sender=sender, receiver=receiver, message="")
        return answer
    
class TagsSerializer(ModelSerializer):
    
    class Meta:
        model = Tags
        fields = "__all__"
        
    def to_internal_value(self, data):
        return data
    
    def validate(self, data):
        is_valid, msg = pydantic_validation(TagValidation, data)
        if not is_valid:
            raise ValidationError({'message':msg})
        return data


class AnswerListSerializer(ModelSerializer):
    
    created = SerializerMethodField()
    updated = SerializerMethodField()
    class Meta:
        model = Answers
        fields = "__all__"
        
    def get_created(self, obj):
        indian_tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        datetime = {
            "date":obj.updated.astimezone(indian_tz).strftime("%Y-%m-%d"),
            "time":obj.updated.astimezone(indian_tz).strftime("%H:%M")
        }
        return datetime

    def get_updated(self, obj):
        indian_tz = zoneinfo.ZoneInfo("Asia/Kolkata")
        datetime = {
            "date":obj.updated.astimezone(indian_tz).strftime("%Y-%m-%d"),
            "time":obj.updated.astimezone(indian_tz).strftime("%H:%M")
        }
        return datetime

class QuestionRelatedAnswersSerializer(Serializer):
    
    question = SerializerMethodField()
    answers = SerializerMethodField()
    
    class Meta:
        fields = [
            'question',
            'answers',
        ]
        
    def get_question(self, obj):
        return ListQuestionSerializer(obj).data
    
    def get_answers(self, obj):
        queryset = Answers.objects.filter(question=obj).order_by('-vote')
        return AnswerListSerializer(queryset, many=True).data
