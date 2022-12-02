from django.db import models


class Question(models.Model):
    title = models.TextField(verbose_name="Question text")

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.TextField(verbose_name="Answer text")
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers",
    )
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.TextField(verbose_name="Name of test")
    questions = models.ManyToManyField(Question, related_name="tests")

    def __str__(self):
        return self.title
