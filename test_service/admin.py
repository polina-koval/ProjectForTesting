from django.contrib import admin
from django.utils.html import format_html

from test_service.models import Answer, Question, Test


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_right")


class AnswerInLine(admin.TabularInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "get_answers")
    inlines = (AnswerInLine,)

    def save_model(self, request, obj, form, change):
        answers = obj.answers.all()
        true_answers = answers.filter(is_right=True).count()
        false_answers = answers.filter(is_right=True).count()
        if not true_answers:
            raise ValueError("At least one answer must be correct.")
        if not false_answers:
            raise ValueError("At least one answer must be wrong.")
        super().save_model(request, obj, form, change)

    def get_answers(self, obj: Question):
        output = [answer.title for answer in obj.answers.all()]
        return format_html("<br />".join(output))

    get_answers.short_description = "Answers"


class QuestionInLine(admin.TabularInline):
    model = Test.questions.through
    extra = 0


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ("title", "get_questions")
    exclude = ("questions", )
    inlines = (QuestionInLine,)

    def get_questions(self, obj: Test):
        output = [question.title for question in obj.questions.all()]
        return format_html("<br />".join(output))

    get_questions.short_description = "Questions"
