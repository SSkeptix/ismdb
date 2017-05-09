from django import forms
from django.contrib.auth.forms import (
	AuthenticationForm,
	UserCreationForm,
	SetPasswordForm
	)
from django.forms.utils import ErrorList
from django.utils.translation import gettext, gettext_lazy as _
from . import models 
from . import tuples

_class = 'form-control'

invalid_characters = '@_+[]\\/0123456789'

password_help_text = '''
			Ваш пароль не може бути схожий на вашу іншу особисту інформацію. <br/>
			Ваш пароль повинен містити як мінімум 8 символів. <br/>
			Ваш пароль не може бути занадто простим (password). <br/>
			Ваш пароль не може складається лише із цифр.
	'''




class Login(AuthenticationForm):
	username = forms.CharField(
		label="Логін",
		max_length=150, 
		widget=forms.TextInput(attrs={
			'class': _class,
			}))

	password = forms.CharField(
		label="Пароль",
		max_length=150, 
		widget=forms.PasswordInput(attrs={
			'class': _class,
			}))





class Registration(UserCreationForm):

	username = forms.CharField(
		label="Логін*",
		help_text = 'Від 5 до 150 символів, використовувати можна латинські букви, цифри і наступні символи: @/./+/-/_',
		max_length=150,
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100_Hacker',
			'class': _class,
			}))

	first_name = forms.CharField(
		label="Ім'я*",
		required = True,
		max_length=150,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петро',
			'class': _class,
			}))

	last_name = forms.CharField(
		label="Прізвище*",
		required = True,
		max_length=150,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петренко',
			'class': _class,
			}))

	email = forms.EmailField(
		label="Email*",
		required = True,
		max_length=150, 
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100hacker@mail.com',
			'class': _class,
			}))

	password1 = forms.CharField(
		label="Пароль*",
		help_text=password_help_text,
		max_length=150, 
		widget=forms.PasswordInput(attrs={
			'placeholder': 'passw@rd',
			'class': _class,
			}))

	password2 = forms.CharField(
		label="Підтвердження паролю*",
		help_text = 'Повторно введіть пароль',
		max_length=150, 
		widget=forms.PasswordInput(attrs={
			'placeholder': 're-enter_passw@rd',
			'class': _class,
			}))

	category = forms.ChoiceField(
		choices = tuples.CATEGORY.SELECT,
		label = 'Категорія*',
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

	def clean_email(self):
		data = self.cleaned_data['email']
		if models.User.objects.filter(email = self.cleaned_data['email']).exists():
			raise forms.ValidationError("Пошта вже зайнята.")
		return data

	def clean_username(self):
		data = self.cleaned_data['username']
		if len(data) < 5:
			raise forms.ValidationError("Ваш логін занадто короткий.")
		return data

	def clean_first_name(self):
		data = self.cleaned_data['first_name']
		for i in data:
			if i in invalid_characters:	
				raise forms.ValidationError("Недопустимі символи.")
		return data

	def clean_last_name(self):
		data = self.cleaned_data['last_name']
		for i in data:
			if i in invalid_characters:	
				raise forms.ValidationError("Недопустимі символи.")
		return data





class SetPassword(SetPasswordForm):
	error_messages = {
		'password_mismatch':  _("The two password fields didn't match."),
	}

	new_password1 = forms.CharField(
		label=_("New password"),
		strip=False,
		help_text=password_help_text,
		widget=forms.PasswordInput(attrs={
			'class': _class,
			}))
	new_password2 = forms.CharField(
		label=_("New password confirmation"),
		strip=False,
		widget=forms.PasswordInput(attrs={
			'class': _class,
			}))





class ChangePassword(SetPassword):
	error_messages = dict(SetPasswordForm.error_messages, **{
		'password_incorrect': _("Your old password was entered incorrectly. Please enter it again."),
	})

	old_password = forms.CharField(
		label=_("Old password"),
		widget=forms.PasswordInput(attrs={
			'class': _class,
			}))

	field_order = ['old_password', 'new_password1', 'new_password2']

	def clean_old_password(self):
		"""
		Validate that the old_password field is correct.
		"""
		old_password = self.cleaned_data["old_password"]
		if not self.user.check_password(old_password):
			raise forms.ValidationError(
				self.error_messages['password_incorrect'],
				code='password_incorrect',
			)
		return old_password