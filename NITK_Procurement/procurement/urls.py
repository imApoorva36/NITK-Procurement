from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name = "register"),
    path("login/", views.login_view, name = "login"),
    path("logout/", views.logout_view, name = "logout"),
    path("fill_form/<int:id>", views.view_form, name = "fill_form"),
    path("pdfgen/<int:id>", views.generate_pdf, name = "generate_pdf"),
    path("create_form/", views.create_form, name="create_form"),
    path("create_section/<int:id>", views.create_section, name = "create_section"),
    path("create_question/<int:id>", views.create_question, name="create_question"),
    path("get_questions/<int:id>", views.get_questions, name="get_questions"),
    path("edit_form/<int:id>", views.edit_form, name="edit_form"),
    path("edit_section/<int:id>", views.edit_section, name="edit_section"),
    path("edit_question/<int:id>", views.edit_question, name="edit_question"),
    path("delete_question/<int:id>", views.delete_question, name="delete_question"),
    path("delete_section/<int:id>", views.delete_section, name="delete_section"),
]
