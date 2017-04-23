from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.User)
admin.site.register(models.Student)

admin.site.register(models.Language)
admin.site.register(models.Framework)
admin.site.register(models.Other)

admin.site.register(models.StudentLanguage)
admin.site.register(models.StudentFramework)
admin.site.register(models.StudentOther)