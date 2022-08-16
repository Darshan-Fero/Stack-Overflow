from django.contrib import admin
from .models import Questions, Answers, Tags

# Register your models here.

class QuestionAdmin(admin.ModelAdmin):
    fields= ('created', 'updated', 'author', 'title', 'body', 'tags', 'vote')
    readonly_fields= ("created", 'updated')
    list_display= ('title', 'body', 'created', 'updated')


admin.site.register(Tags)
admin.site.register(Questions, QuestionAdmin)
admin.site.register(Answers)
