from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from account import models 
from account import tuples


class EditUser(forms.ModelForm):
	_class = 'form-control'

	username = forms.CharField(
		label="Username",
		help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100_Hacker',
			'class': _class,
			'name': 'username'
			}))

	first_name = forms.CharField(
		label="First_name",
		required = True,
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петро',
			'class': _class,
			'name': 'first_name'
			}))

	last_name = forms.CharField(
		label="Last_name",
		required = True,
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петренко',
			'class': _class,
			'name': 'last_name'
			}))

	email = forms.EmailField(
		label="Email",
		required = True,
		max_length=50, 
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100hacker@mail.com',
			'class': _class,
			'name': 'email'
			}))

	class Meta:
		model = models.User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			)



class EditStudent(forms.ModelForm):
	_class = 'form-control'

	lang = forms.ChoiceField(
		choices = tuples.LANG.SELECT,
		label = 'English level',
		required = True,
		widget=forms.Select(attrs={
			'class': _class,
			'style': 'width:auto;'
			}))


	github = forms.URLField(
		label="GitHub",
		required = False,
		max_length=200, 
		widget=forms.TextInput(attrs={
			'class': _class,
			'name': 'github'
			}))

	group = forms.CharField(
		label="Group",
		required = True,
		max_length=50, 
		widget=forms.TextInput(attrs={
			'class': _class,
			'name': 'group'
			}))


	description = forms.CharField(
		label = 'Describe yourself',
		required = False,
		max_length=2000,
		widget=forms.Textarea(attrs={
			'class': _class,
			}))

	class Meta:
		model = models.StudentProfile
		fields = (
			'lang',
			'group',
			'github',
			'description',
			)



class AddStudent(EditStudent):
	user = None

	class Meta:
		model = models.StudentProfile
		fields = (
			'lang',
			'group',
			'github',
			'description',
			)	

	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(AddStudent, self).__init__(*args, **kwargs)

	def is_valid(self):
		valid = super(AddStudent, self).is_valid()
		if not valid:
			return valid
		if models.Student.objects.filter(user = self.user).exists():
			self._errors['profile_exists'] = 'Profile is already exist. Close this page.'
			return False
		return True

	def save(self, commit=True):
		instance = super(AddStudent, self).save(commit=False)
		instance.user = self.user

		if commit:
			instance.save()
		return instance



# base form for all type of skill
class Skill(forms.ModelForm):
	student = None

	def __init__(self, *args, **kwargs):
		self.student = kwargs.pop('student', None)
		super(Skill, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		instance = super(Skill, self).save(commit=False)
		if self.student == models.Student:
			instance.student = self.student
		else:
			instance.student = models.Student.objects.get(user__id = self.student.user.id)

		if commit:
			instance.save()
		return instance


class Lang(Skill):
	class Meta:
		model = models.Student_lang
		exclude = (
			'student',
			'validated_by', 
			'validated_at',
			)

	def is_valid(self):
		valid = super(Lang, self).is_valid()
		if not valid:
			return valid
		if models.Student_lang.objects.filter(student = self.student.user.id, skill = self.cleaned_data['skill']).count():
			self._errors['skill_exists'] = 'Skill is already exist'
			return False
		return True


class Fram(Skill):
	class Meta:
		model = models.Student_fram
		exclude = (
			'student',
			'validated_by', 
			'validated_at',
			)

	def is_valid(self):
		valid = super(Fram, self).is_valid()
		if not valid:
			return valid
		if models.Student_fram.objects.filter(student = self.student.user.id, skill = self.cleaned_data['skill']).count():
			self._errors['skill_exists'] = 'Skill is already exist'
			return False
		return True

class Other(Skill):
	class Meta:
		model = models.Student_other
		exclude = (
			'student',
			'validated_by', 
			'validated_at',
			)

	def is_valid(self):
		valid = super(Other, self).is_valid()
		if not valid:
			return valid
		if models.Student_other.objects.filter(student = self.student.user.id, skill = self.cleaned_data['skill']).count():
			self._errors['skill_exists'] = 'Skill is already exist'
			return False
		return True
