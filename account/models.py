from django.db import models
from django.contrib.auth.models import AbstractUser
from . import tuples



#custom User
class User(AbstractUser):
	is_validate = models.BooleanField(default = False)
	category = models.IntegerField(choices=tuples.CATEGORY.SELECT, default=tuples.CATEGORY.STUDENT)

	def __str__(self):
		return str(self.get_username())


# extra field for user - Student
class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
	lang = models.IntegerField(choices=tuples.LANG.SELECT, default=tuples.LANG.A1)
	group = models.CharField(max_length = 50, null = True)
	validate_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='validate_by', null = True, blank = True)
	updated = models.DateField(auto_now=True)

	github = models.URLField(null = True, blank = True, unique = True)
	description = models.TextField(max_length = 2000, null = True, blank = True)


	def get_username(self):
		return self.user.get_username()

	def __str__(self):
		return str(self.get_username())




#
#	--- Student skills ---
#



# abstract model for
#					 - programing languages
#					 - programing fraimworks
#					 - other skills
class Skill(models.Model):
	value = models.CharField(max_length = 50, unique = True)
	validate_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
	validate_at = models.DateField(auto_now=True)

	class Meta:
		abstract = True

	def get_value(self):
		return self.value

	def __str__(self):
		return str(self.get_value())




#programing languages model
class Language(Skill):
	pass

#programing fraimworks model
class Framework(Skill):
	lang = models.ForeignKey(Language, on_delete=models.CASCADE)

	def get_lang(self):
		return self.lang.get_value()

	def __str__(self):
		return str("%s - %s" % (self.get_lang(), self.get_value()))

#other skills model
class Other(Skill):
	pass





# abstract model for student skills
class Student_skill(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	validate_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)
	validate_at = models.DateField(auto_now=True)
	show = models.BooleanField(default = True)

	class Meta:
		abstract = True
		unique_together = ('student', 'skill')

	def __str__(self):
		return str("%s - %s" % (self.student.get_username(), self.skill.get_value()) )




# student - language
class Student_lang(Student_skill):
	skill = models.ForeignKey(Language, on_delete=models.CASCADE)


# student - framework
class Student_fram(Student_skill):
	skill = models.ForeignKey(Framework, on_delete=models.CASCADE)


# student - other
class Student_other(Student_skill):
	skill = models.ForeignKey(Other, on_delete=models.CASCADE)

#
#	--- Student skills - end ---
#
