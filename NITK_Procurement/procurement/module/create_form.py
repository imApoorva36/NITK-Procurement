def create_form(request) :
    if request.method == "GET" :
        return render(request, "procurement/create_form.html")
    else :
        outside_title = request.POST["outside_title"]
        in_title = request.POST["in_title"]
        description = request.POST["description"]
        is_active = request.POST["is_active"] == "on"
        line_below = request.POST["line_below"] == "on"

        new_form = Form(
            form_owner = request.user,
            outside_title = outside_title,
            in_title = in_title,
            description = description,
            is_active = is_active,
            line_below = line_below
        )
        new_form.save()
        return HttpResponseRedirect(reverse(home))

from django.http import JsonResponse

def create_section(request, id):
    get_form = Form.objects.get(id=id)
    all_forms = Form.objects.filter(is_active = True)
    if request.method == "GET":
        return render(request, "procurement/create_section.html", {
            "form": get_form,
            "all_forms": all_forms
        })
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        section_type = request.POST["section_type"]
        bold = request.POST["bold"] == "on"
        line_below = request.POST.get("line_below", False) == "on"

        new_sec = Section(
            title=title,
            description=description,
            section_type=section_type,
            form=get_form,
            bold = bold,
            line_below = line_below
        )
        new_sec.save()

        # Send a JSON response with the ID of the newly created section
        response_data = {'section_id': new_sec.id}
        return JsonResponse(response_data)

def create_question(request, id):
    if request.method == "POST" :
        get_sec = Section.objects.get(id = id)
        question = request.POST["question"]
        align_type = request.POST["align_type"]
        bold = request.POST["bold_ques"] == "on"
        self_question_id = request.POST["questions"]
        self_question = Question.objects.get(id = self_question_id)
        form = get_sec.form
        new_ques = Question (
            question = question,
            section = get_sec,
            form = form,
            align_type = align_type,
            bold = bold,
            self_question = self_question
        )
        new_ques.save()
        response_data = {'message': "Successfull"}
        return JsonResponse(response_data)

def get_questions(request, id) :
    if request.method == "POST" :
        get_form = Form.objects.get(id = id)
        all_questions = get_form.questions.all()
        response = {str(question.id): question.question for question in all_questions}

        return JsonResponse(response)
# URLs

    # path("create_form/", views.create_form, name="create_form"),
    # path("create_section/<int:id>", views.create_section, name = "create_section"),
    # path("create_question/<int:id>", views.create_question, name="create_question"),
    # path("get_questions/<int:id>", views.get_questions, name="get_questions"),
