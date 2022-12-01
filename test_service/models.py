from django.db import models


class Question(models.Model):
    title = models.TextField()

    def __str__(self):
        return self.title


class Answer(models.Model):
    title = models.TextField()
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    is_right = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Test(models.Model):
    title = models.TextField()
    questions = models.ManyToManyField(Question)

    def __str__(self):
        return self.title
