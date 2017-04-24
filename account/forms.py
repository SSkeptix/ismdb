from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from . import models 
from . import tuples

_class = 'form-control'





class Login(AuthenticationForm):
	username = forms.CharField(
		label="Username",
		max_length=150, 
		widget=forms.TextInput(attrs={
			'class': _class,
			}))

	password = forms.CharField(
		label="Password",
		max_length=150, 
		widget=forms.PasswordInput(attrs={
			'class': _class,
			}))





class Registration(UserCreationForm):

	username = forms.CharField(
		label="Логін",
		help_text = '150 символів або менше, використовувати можна латинські букви, цифри і наступні символи: @/./+/-/_',
		max_length=150,
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100_Hacker',
			'class': _class,
			}))

	first_name = forms.CharField(
		label="Ім'я",
		required = True,
		max_length=150,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петро',
			'class': _class,
			}))

	last_name = forms.CharField(
		label="Прізвище",
		required = True,
		max_length=150,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петренко',
			'class': _class,
			}))

	email = forms.EmailField(
		label="Email",
		required = True,
		max_length=150, 
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100hacker@mail.com',
			'class': _class,
			}))

	password1 = forms.CharField(
		label="Password",
		help_text = '''
			Ваш пароль не може бути схожий на вашу іншу особисту інформацію. <br/>
			Ваш пароль повинен містити не менше 8 символів. <br/>
			Ваш пароль не може бути занадто простим (password). <br/>
			Ваш пароль не може бути повністю числовим.
		''',
		max_length=150, 
		widget=forms.PasswordInput(attrs={
			'placeholder': 'passw@rd',
			'class': _class,
			}))

	password2 = forms.CharField(
		label="Підтвердження паролю",
		help_text = 'Повторно введіть пароль',
		max_length=150, 
		widget=forms.PasswordInput(attrs={
			'placeholder': 're-enter_passw@rd',
			'class': _class,
			}))

	category = forms.ChoiceField(
		choices = tuples.CATEGORY.SELECT,
		label = 'Категорія',
		required = True,
		widget=forms.Select(attrs={
			'class': _class,
			'style': 'width:auto;'
			}))

	class Meta:
		model = models.User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
			'category',
			)

	def save(self, commit=True):
		user = super(Registration, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.category = self.cleaned_data['category']	

		if commit:
			user.save()

		return user

	def is_valid(self):
		valid = super(Registration, self).is_valid()
		if not valid:
			return valid
		if models.User.objects.filter(email = self.cleaned_data['email']).exists():
			self._errors['email_exists'] = 'Email is already exist'
			return False
		return True
