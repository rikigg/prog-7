from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from polls import views as polls_views

urlpatterns = [
    path("polls/", include("polls.urls")),
    path("admin/", admin.site.urls),
    path("register/", polls_views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(
        template_name="polls/login.html"
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(
        template_name="polls/logged_out.html",
        next_page="polls:index"
    ), name="logout"),
    path("", polls_views.IndexView.as_view(), name="index"),
]