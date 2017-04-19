from django.contrib import admin
from .models import User, Student, StudentProfile, Language, Framework, Other, Student_lang, Student_fram, Student_other
# Register your models here.

admin.site.register(User)
admin.site.register(Student)
admin.site.register(StudentProfile)

admin.site.register(Language)
admin.site.register(Framework)
admin.site.register(Other)

admin.site.register(Student_lang)
admin.site.register(Student_fram)
admin.site.register(Student_other)