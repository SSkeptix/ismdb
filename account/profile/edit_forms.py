from django import forms
from account import models 
from account import tuples

_class = 'form-control'




class EditUser(forms.ModelForm):
	username = forms.CharField(
		label="Логін",
		help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100_Hacker',
			'class': _class,
			}))

	first_name = forms.CharField(
		label="Ім'я",
		required = True,
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петро',
			'class': _class,
			}))

	last_name = forms.CharField(
		label="Прізвище",
		required = True,
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петренко',
			'class': _class,
			}))

	email = forms.EmailField(
		label="Email",
		required = True,
		max_length=50, 
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100hacker@mail.com',
			'class': _class,
			}))

	class Meta:
		model = models.User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			)

	def is_valid(self):
		valid = super(EditUser, self).is_valid()
		if not valid:
			return valid
		if models.User.objects.exclude(username=self.cleaned_data['username']).filter(email=self.cleaned_data['email']).exists():
			self._errors['email_exists'] = 'Email is already exist.'
			return False
		return True





class EditStudent(forms.ModelForm):
	english = forms.ChoiceField(
		choices = tuples.ENGLISH.SELECT,
		label = 'Рівень англійської',
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
			}))

	group = forms.CharField(
		label="Група",
		required = True,
		max_length=50, 
		widget=forms.TextInput(attrs={
			'class': _class,
			}))


	description = forms.CharField(
		label = 'Опиши себе',
		required = False,
		max_length=2000,
		widget=forms.Textarea(attrs={
			'class': _class,
			}))

	class Meta:
		model = models.Student
		fields = (
			'english',
			'group',
			'github',
			'description',
			)