from django.db import models
from django.contrib.auth.models import AbstractUser
from . import tuples





#custom User
class User(AbstractUser):
	category = models.IntegerField(choices=tuples.CATEGORY.SELECT, default=tuples.CATEGORY.STUDENT)
	validated_by = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='validate_by', null = True, blank = True)

	def __str__(self):
		return str(self.get_full_name())





# extra field for user - Student
class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
	english = models.IntegerField(choices=tuples.ENGLISH.SELECT, default=tuples.ENGLISH.A1)
	group = models.CharField(max_length = 50, null = True)
	github = models.URLField(null = True, blank = True)
	description = models.TextField(max_length = 2000, null = True, blank = True)

	def __str__(self):
		return str(user.__str__())





class Skill(models.Model):
	value = models.CharField(max_length = 50, unique = True)
	validated_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
	updated = models.DateField(auto_now=True)

	def __str__(self):
		return str(self.value)





class StudentSkill(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)
	updated = models.DateField(auto_now=True)
	skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('student', 'skill')

	def __str__(self):
		return str('{0} - {1}'.format(self.student.__str__(), self.skill.__str__()) )
