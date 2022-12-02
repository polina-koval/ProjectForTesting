from django.contrib.auth import views as auth_views
from django.urls import path

from test_service.views import TestDetailView, TestListView, register_request

urlpatterns = [
    path("register", register_request, name="register"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="test_service/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(
            template_name="test_service/logout.html"
        ),
        name="logout",
    ),
    path("", TestListView.as_view(), name="test_list"),
    path("test/<pk>/", TestDetailView.as_view(), name="test_detail"),
]
