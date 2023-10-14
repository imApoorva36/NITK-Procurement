from django.db import models
from django.contrib.auth.models import User

class Form(models.Model) :
    form_owner = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name="created_forms")
    outside_title = models.CharField(max_length=100, null=True, blank=True)
    in_title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) :
        return self.outside_title

class Section(models.Model) :
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="sections")
    section_type = models.CharField(max_length=50)

    def __str__(self) :
        return self.form.outside_title

class Question(models.Model) :
    question = models.CharField(max_length=500)
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name="questions")
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="questions")
    type = models.CharField(max_length=100, null=True, blank=True)
    self_question = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="question_related")
    answer_required = models.BooleanField(default=True)
    option1 = models.CharField(max_length=100, null=True, blank=True)
    option2 = models.CharField(max_length=100, null=True, blank=True)
    option3 = models.CharField(max_length=100, null=True, blank=True)
    option4 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self) :
        return self.question

class Response(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="responses")
    body = models.CharField(max_length=100)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="responses")
    form = models.ForeignKey(Form, on_delete=models.CASCADE, related_name="responses")

    def __str__(self) :
        return self.body
