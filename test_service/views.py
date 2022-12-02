from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from test_service.models import Answer, Question, Test

from .forms import NewUserForm


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("test_list")
        messages.error(
            request, "Unsuccessful registration. Invalid information."
        )
    form = NewUserForm()
    return render(
        request=request,
        template_name="test_service/register.html",
        context={"register_form": form},
    )


class TestDetailView(DetailView):
    model = Test
    context_object_name = "test"
    template_name = "test_service/detail_test.html"

    def post(self, request, pk):
        total = 0
        answers = request.POST.getlist("answer")
        answers_objects = Answer.objects.filter(pk__in=answers)
        questions = Question.objects.filter(
            pk__in=answers_objects.values_list("question__pk")
        )
        test = Test.objects.get(pk=pk)
        if list(questions) == list(test.questions.all()):
            for q in questions:
                if set(q.answers.filter(is_right=True)).issubset(
                    set(answers_objects)
                ):
                    total += 1
            return HttpResponse(
                f"Your result: {total}/{test.questions.count()}",
                content_type="text/plain",
            )
        return HttpResponseBadRequest("You didn't answer all the questions.")


class TestListView(ListView):
    queryset = Test.objects.all()
    context_object_name = "tests"
    template_name = "test_service/list_test.html"
