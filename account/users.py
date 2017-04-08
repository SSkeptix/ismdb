from django.db import models
from django.contrib.auth.models import AbstractUser

class GROUP:
	STUDENT = 1
	TEACHER = 2
	EMPLOYER = 3

	SELECT = (
		(STUDENT, 'Student'),
		(TEACHER, 'Teacher'),
		(EMPLOYER, 'Employer'),
	)

class User(AbstractUser):
	is_validate = models.BooleanField(default = False)
	group = models.IntegerField(choices=GROUP.SELECT, default=GROUP.STUDENT)

	def __str__(self):
		return str(self.get_username())



# user --- Student

class LANG:
	A1 = 1
	A2 = 2
	B1 = 3
	B2 = 4
	C1 = 5
	C2 = 6

	SELECT = (
		(A1, 'A1 - Elementary'), 
		(A2, 'A2 - Pre-Intermediate'), 
		(B1, 'B1 - Intermediate'), 
		(B2, 'B2 - Upper intermediate'),
		(C1, 'C1 - Advanced'), 
		(C2, 'C2 - Proficient'),
	)

class Student(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	lang = models.IntegerField(choices=LANG.SELECT, default=LANG.A1)
	group = models.CharField(max_length = 10, null = True)

	def get_username(self):
		return self.user.get_username()

	def __str__(self):
		return str(self.get_username())


class Skill(models.Model):
	value = models.CharField(max_length = 30, unique = True)

	def get_value(self):
		return self.value

	def __str__(self):
		return str(self.value)

class Student_skill(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
	validate_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)

	class Meta:
		unique_together = ('student', 'skill')


	def __str__(self):
		return str("%s - %s" % (self.student.get_username(), self.skill.get_value()) )
