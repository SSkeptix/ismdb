from django.contrib import admin
from .models import User, Student, StudentProfile, Language, Framework, Other, Student_lang, Student_fram, Student_other
# Register your models here.

admin.site.register(User)
admin.site.register(Student)

admin.site.register(Language)
admin.site.register(Framework)
admin.site.register(Other)

admin.site.register(StudentLanguage)
admin.site.register(StudentFramework)
admin.site.register(StudentOther)