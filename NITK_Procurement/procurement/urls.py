from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name = "register"),
    path("login/", views.login_view, name = "login"),
    path("logout/", views.logout_view, name = "logout"),
    path("fill_form/<int:id>", views.view_form, name = "fill_form"),
]
