from django.db import models


class StudentSkill(models.Manager):
	def get_queryset(self, student, show = False):
		return super(StudentSkill, self).get_queryset().filter(student = student, show = show)

		