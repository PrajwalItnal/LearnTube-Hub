from django.contrib import admin
from .models import Courses, Profile, Enrollment, Certificate

# Register your models here.
admin.site.register(Profile)
admin.site.register(Courses)
admin.site.register(Enrollment)
admin.site.register(Certificate)