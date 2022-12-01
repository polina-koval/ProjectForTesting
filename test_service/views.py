from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView

from test_service.models import Test

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


class TestListView(ListView):
    queryset = Test.objects.all()
    context_object_name = "tests"
    template_name = "test_service/list_test.html"
