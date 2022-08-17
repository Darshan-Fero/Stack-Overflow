from django.contrib import admin
from .models import AnswersVote, Questions, Answers, QuestionsVote, Tags

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    fields= ('created', 'updated', 'author', 'title', 'body', 'tags', 'vote')
    readonly_fields= ("created", 'updated')
    list_display= ('title', 'body', 'created', 'updated')
    
class AnswersAdmin(admin.ModelAdmin):
    fields= ('created', 'updated', 'author', 'question', 'body', 'vote', 'is_approved')
    readonly_fields= ("created", 'updated')
    


admin.site.register(Tags)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(Answers, AnswersAdmin)
admin.site.register(QuestionsVote)
admin.site.register(AnswersVote)
