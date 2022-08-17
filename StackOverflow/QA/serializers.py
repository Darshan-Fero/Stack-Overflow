import zoneinfo
from rest_framework.serializers import Serializer, ListField, ModelSerializer, ValidationError, SerializerMethodField, HyperlinkedModelSerializer
from user.utils import pydantic_validation
from .models import Answers, AnswersVote, Questions, QuestionsVote, Tags
from .pydantics import QuestionValidation, AnswerValidation, QuestionsVoteValidation, TagValidation
from .tasks import sendEmail

class TagSerializer(ModelSerializer):
    class Meta:
        model = Tags
        fields= "__all__"

class CreateQuestionSerializer(ModelSerializer):
    
    tags = ListField(required=False, write_only=True)
    assosiated_tags = SerializerMethodField()
    class Meta:
        model = Questions
        fields = (
            'id',
            'author',
            'title',
            'body',
            'assosiated_tags',
            'tags'
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
        tag_list = []
        for tag in validated_data['tags']:
            tag_list.append(Tags.objects.filter(name__iexact=tag).first())
        validated_data.pop('tags')
        validated_data.update({'author':request.user})
        question = Questions(**validated_data)
        question.save()
        question.tags.set(tag_list)
        question.save()
        return question
    
    def update(self, instance, validated_data):
        if validated_data.get('tags'):
            tag_list=[]
            for tag in validated_data['tags']:
                tag_list.append(Tags.objects.filter(name__iexact=tag).first())
            instance.tags.set(tag_list)
        instance.title = validated_data.get('title') or instance.title
        instance.body = validated_data.get('body') or instance.body
        instance.save()
        return instance
    
    def get_assosiated_tags(self, obj):
        tag_list=obj.tags.all()
        return TagSerializer(tag_list, many=True).data


class ListQuestionSerializer(ModelSerializer):
    
    tags = SerializerMethodField()
    created = SerializerMethodField()
    updated = SerializerMethodField()
    class Meta:
        model = Questions
        fields = ('id', 'slug', 'author', 'title', 'body', 'tags', 'vote', 'created', 'updated')
        
    def get_tags(self, obj):
        tag_list=[]
        for i in obj.tags.get_queryset():
            tag_list.append(i.name)
        return tag_list
    
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


class VoteToQuestionSerializer(ModelSerializer):
    
    class Meta:
        model = QuestionsVote
        fields = ['user', 'vote']
        
    def to_internal_value(self, data):
        return data
    
    def validate(self, data):
        print(data)
        is_valid, msg = pydantic_validation(QuestionsVoteValidation, data)
        if not is_valid:
            raise ValidationError({'message':msg})
        return data
    
    def questionVote(self, validate_data):
        question = Questions.objects.get(pk=int(validate_data.get('question')))
        validate_data.update({'question':question})
        instance = QuestionsVote.objects.filter(user=validate_data.get('user'), question=question).first()
        if instance:
            return self.update(instance, validate_data)
        question_vote = QuestionsVote(**validate_data)
        question_vote.save()
        return question_vote
    
    def answerVote(self, validate_data):
        answer = Answers.objects.get(pk=int(validate_data.get('answer')))
        validate_data.update({'answer':answer})
        instance = AnswersVote.objects.filter(user=validate_data.get('user'), answer=answer).first()
        if instance:
            return self.update(instance, validate_data)
        question_vote = AnswersVote(**validate_data)
        question_vote.save()
        return question_vote
    
    def create(self, validate_data):
        request = self.context.get('request')
        validate_data.update({'user':request.user})
        validate_data.update({'vote':str(validate_data['vote']).upper()})
        if validate_data.get('question'):
            return self.questionVote(validate_data)
        else:
            return self.answerVote(validate_data)

    def update(self, instance, validate_data):
        if instance.vote == validate_data.get('vote'):
            return instance
        instance.vote = validate_data.get('vote')
        instance.save()
        return instance