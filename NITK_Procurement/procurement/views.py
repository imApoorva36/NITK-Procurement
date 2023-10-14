from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Form, Section, Question, Response
import datetime


# Create your views here.

def home(request) :
    if not request.user.is_authenticated :
        return HttpResponseRedirect(reverse(login_view))
    else :
        active_forms = Form.objects.filter(is_active = True)
        return render(request, "procurement/home.html", {
            "forms" : active_forms
        })

def register_view(request) :
    if not request.user.is_authenticated:
        if request.method == "POST" :
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            confirm_password = request.POST["confirm_password"]

            if password != confirm_password :
                return render(request, "procurement/register.html", {
                    "message" : "Password does not match"
                })

            try :
                user = User.objects.create_user(username, email, password)
                user.save()

            except IntegrityError:
                return render(request, "procurement/register.html", {
                    "message" : "A user with that username already exist"
                })

            login(request, user)
            return HttpResponseRedirect(reverse(home))

        else:
            return render(request, "procurement/register.html")
    else:
        return HttpResponseRedirect(reverse(home))

def login_view(request) :
    if not request.user.is_authenticated:
        if request.method == "POST" :
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)

            if user is not None :
                login(request, user)
                return HttpResponseRedirect(reverse(home))
            else :
                return render(request, "procurement/login.html", {
                    "message" : "Invalid username and/or password."
                })

        else :
            return render(request, "procurement/login.html")
    else :
        return HttpResponseRedirect(reverse(home))

def logout_view(request) :
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect(reverse(login_view))

def view_form(request, id) :
    if request.user.is_authenticated :
        get_form = Form.objects.get(id = id)
        get_sections = Section.objects.filter(form = get_form)
        # if request.method == "GET" :
        #     if request.user in get_form.responses : Need to do this later if required..
        if request.method == "GET" :
            return render(request, "procurement/form.html", {
                "form" : get_form,
                "sections" : get_sections
            })
        else :
            all_questions = Question.objects.filter(form = get_form)
            for question in all_questions :
                if question.answer_required :
                    response_for_question = request.POST.get("question" + str(question.id))
                    new_response = Response(
                        form = get_form,
                        body = response_for_question,
                        user = request.user,
                        question = question
                     )
                    new_response.save()
            return HttpResponseRedirect(reverse(home))
