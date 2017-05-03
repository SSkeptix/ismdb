from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Student)
admin.site.register(models.Skill)
admin.site.register(models.StudentSkill)
