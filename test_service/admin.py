from django.contrib import admin

from test_service.models import Answer, Question, Test


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    pass


class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ["title"]
    inlines = (AnswerInLine,)


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass
