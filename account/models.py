from django.db import models
from django.contrib.auth.models import AbstractUser
from . import tuples





#custom User
class User(AbstractUser):
	category = models.IntegerField(choices=tuples.CATEGORY.SELECT, default=tuples.CATEGORY.STUDENT)
	validated_by = models.ForeignKey('User', on_delete=models.SET_NULL, related_name='validate_by', null = True, blank = True)

	def __str__(self):
		return str(self.get_username())





# extra field for user - Student
class Student(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
	english = models.IntegerField(choices=tuples.ENGLISH.SELECT, default=tuples.ENGLISH.A1)
	group = models.CharField(max_length = 50, null = True)
	github = models.URLField(null = True, blank = True)
	description = models.TextField(max_length = 2000, null = True, blank = True)

	def get_username(self):
		return self.user.username

	def __str__(self):
		return str(self.get_username())



# abstract model for
#					 - programing languages
#					 - programing fraimworks
#					 - other skills
class SkillBase(models.Model):
	value = models.CharField(max_length = 50, unique = True)
	validated_by = models.ForeignKey(User, on_delete=models.CASCADE, null = True, blank = True)
	validated_at = models.DateField(auto_now=True)

	class Meta:
		abstract = True

	def get_value(self):
		return self.value

	def __str__(self):
		return str(self.get_value())


#programing languages model
class Language(SkillBase):
	pass

#programing fraimworks model
class Framework(SkillBase):
	value = models.CharField(max_length = 50)
	lang = models.ForeignKey(Language, on_delete=models.CASCADE)

	class Meta:
		unique_together = ('value', 'lang')

	def get_lang(self):
		return self.lang.get_value()

	def __str__(self):
		return str("%s - %s" % (self.get_lang(), self.get_value()))

#other skills model
class Other(SkillBase):
	pass





# abstract model for student skills
class StudentSkill(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	validated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null = True, blank = True)
	validated_at = models.DateField(auto_now=True)

	class Meta:
		abstract = True
		unique_together = ('student', 'skill')

	def __str__(self):
		return str("%s - %s" % (self.student.get_username(), self.skill.get_value()) )

class StudentLanguage(StudentSkill):
	skill = models.ForeignKey(Language, on_delete=models.CASCADE)

class StudentFramework(StudentSkill):
	skill = models.ForeignKey(Framework, on_delete=models.CASCADE)

class StudentOther(StudentSkill):
	skill = models.ForeignKey(Other, on_delete=models.CASCADE)
