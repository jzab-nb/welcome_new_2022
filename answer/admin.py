from django.contrib import admin
from .models import StudentTest, Test, Question

admin.site.register(Question)
admin.site.register(Test)
admin.site.register(StudentTest)
