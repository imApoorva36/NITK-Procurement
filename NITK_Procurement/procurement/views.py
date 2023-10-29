from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import Form, Section, Question, Response
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse
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

from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

def view_form(request, id) :
    if request.user.is_authenticated :
        get_form = Form.objects.get(id = id)
        get_sections = Section.objects.filter(form = get_form)
        questions = Question.objects.filter(form = get_form)
        self_question_response = {}
        for question in questions :
            if question.self_question :
                self_question_response[question.id] = Response.objects.get(user = request.user, question = question.self_question)

        if request.method == "GET" :
            user_responses = Response.objects.filter(form = get_form, user = request.user)
            if user_responses.exists() :    
                all_responses = {}
                for response in user_responses :
                    all_responses[response.question.id] = response.body
                return render(request, "procurement/view_form.html", {
                    "form" : get_form,
                    "sections" : get_sections,
                    "responses" : all_responses,
                    "self_question" : self_question_response
                })
            else :
                return render(request, "procurement/form.html", {
                    "form" : get_form,
                    "sections" : get_sections,
                    "self_question" : self_question_response
                })
        else :
            all_questions = Question.objects.filter(form = get_form)
            user_responses = Response.objects.filter(form = get_form, user = request.user)
            if user_responses.exists() :
                for question in all_questions :
                    if question.answer_required :
                        existing_response = Response.objects.get(form = get_form, user = request.user, question = question)
                        edited_response_body = request.POST.get("question" + str(question.id))
                        existing_response.body = edited_response_body
                        existing_response.save()
                return HttpResponseRedirect(reverse(view_form, args=(id, )))

            else :
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

def generate_pdf(request, id):
    if request.user.is_authenticated:
        get_form = Form.objects.get(id = id)
        get_sections = Section.objects.filter(form = get_form)
        questions = Question.objects.filter(form = get_form)
        self_question_response = {}
        for question in questions :
            if question.self_question :
                self_question_response[question.id] = Response.objects.get(user = request.user, question = question.self_question)
            user_responses = Response.objects.filter(form = get_form, user = request.user)
            if user_responses.exists() :    
                all_responses = {}
                for response in user_responses :
                    all_responses[response.question.id] = response.body
        if request.method == 'POST':
            context = {
                'self_question_response': self_question_response,
                'all_responses': all_responses,
            }
            template = get_template('procurement/pdfgen.html')  # Use f-string to include id in the template path
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="Document_Generated.pdf"'
            pisa.CreatePDF(html, dest=response)
            return response
