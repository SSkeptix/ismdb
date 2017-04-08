from django.contrib import admin
from .users import User, Skill, Student, Student_skill
# Register your models here.

admin.site.register(User)
admin.site.register(Skill)
admin.site.register(Student)
admin.site.register(Student_skill)