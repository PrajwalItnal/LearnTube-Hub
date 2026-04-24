from django.contrib import admin
from .models import Courses, Profile, Enrollment, Certificate, Module, Lesson, LessonProgress

# Register your models here.
admin.site.register(Profile)
admin.site.register(Courses)
admin.site.register(Module)
admin.site.register(Lesson)
admin.site.register(Enrollment)
admin.site.register(LessonProgress)
admin.site.register(Certificate)
