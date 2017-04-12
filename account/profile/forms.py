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

	lang = forms.ChoiceField(
		choices = tuples.LANG.SELECT,
		label = 'English level',
		required = True,
		widget=forms.Select()
		)

	github = forms.CharField(
		label="GitHub",
		required = False,
		max_length=200, 
		widget=forms.TextInput(attrs={
			'class': 'form-control',
			'name': 'github'
			}))

	group = forms.CharField(
		label="Group",
		required = True,
		max_length=50, 
		widget=forms.TextInput(attrs={
			'class': 'form-control',
			'name': 'group'
			}))


	description = forms.CharField(
		label = 'Describe yourself',
		required = False,
		max_length=2000,
		widget=forms.Textarea(attrs={
			'class': 'form-control'
			}))

	class Meta:
		model = models.Student
		fields = (
			'lang',
			'group',
			'github',
			'description',
			)



class Lang(forms.ModelForm):
	class Meta:
		model = models.Student_lang
		exclude = (
			'student',
			'validated_by', 
			'validated_at',
			)

	def save(self, commit=True):
		student = super(Add_lang, self).save(commit=False)

		student.skill = self.cleaned_data['skill']

		if commit:
			student.save()

		return student



class Fram(forms.ModelForm):
	class Meta:
		model = models.Student_fram
		exclude = (
			'student',
			'validated_by', 
			'validated_at',
			)

	def save(self, commit=True):
		student = super(Add_fram, self).save(commit=False)

		student.lang = self.cleaned_data['lang']
		student.skill = self.cleaned_data['skill']

		if commit:
			student.save()

		return student


class Other(forms.ModelForm):
	class Meta:
		model = models.Student_other
		exclude = (
			'student',
			'validated_by', 
			'validated_at',
			)

	def save(self, commit=True):
		student = super(Add_other, self).save(commit=False)

		student.skill = self.cleaned_data['skill']

		if commit:
			student.save()

		return student


class Skill(forms.Form):
	fram = Fram()
	lang = Lang()
	other = Other()

	skill = forms.ChoiceField(
		choices = tuples.SKILL.SELECT,
		label = 'Add skill',
		required = True,
		widget=forms.Select()
		)

	class Meta:
		field = ('skill', )

	def __init__(self, fram, lang, other):
		self.fram = fram
		self.lang = lang
		self.other = other

	def save(self, commit=True):

		if commit:
			self.fram.save()
			self.lang.save()
			self.other.save()
