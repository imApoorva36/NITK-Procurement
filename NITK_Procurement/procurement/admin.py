from django.contrib import admin
from .models import Form, Question, Section, Response

admin.site.register(Form)
admin.site.register(Section)
admin.site.register(Question)
admin.site.register(Response)
