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

    def save_model(self, request, obj, form, change):
        answers_count = obj.answers.filter(is_right=True).count()
        print(answers_count)
        if answers_count > 0:
            super().save_model(request, obj, form, change)
        else:
            raise ValueError("At least one answer must be correct.")


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    pass
