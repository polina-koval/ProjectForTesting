from django.contrib import admin
from django.utils.html import format_html

from test_service.models import Answer, Question, Test


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ("title", "is_right", "question")


class AnswerInLine(admin.StackedInline):
    model = Answer
    extra = 0


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("title", "get_answers")
    inlines = (AnswerInLine,)

    def save_formset(self, request, form, formset, change):
        """
        Does not save questions with only incorrect and only correct answers.
        There must be at least one right and wrong answer.
        """
        formset.save()
        true_answers, false_answers = 0, 0
        for f in formset.forms:
            obj = f.instance
            if obj.is_right:
                true_answers += 1
            else:
                false_answers += 1
            obj.user = request.user
            obj.save()
        if not true_answers:
            raise ValueError("At least one answer must be correct.")
        if not false_answers:
            raise ValueError("At least one answer must be wrong.")

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
