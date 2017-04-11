from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from . import models 

class Login(AuthenticationForm):
	username = forms.CharField(
		label="Username",
		max_length=50, 
		widget=forms.TextInput(attrs={
			'class': 'form-control',
			'name': 'username'
			}))

	password = forms.CharField(
		label="Password",
		max_length=50, 
		widget=forms.PasswordInput(attrs={
			'class': 'form-control',
			'name': 'password'
			}))


class Registration(UserCreationForm):
	username = forms.CharField(
		label="Username",
		help_text = 'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100_Hacker',
			'class': 'form-control',
			'name': 'username'
			}))

	first_name = forms.CharField(
		label="First_name",
		required = True,
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петро',
			'class': 'form-control',
			'name': 'first_name'
			}))

	last_name = forms.CharField(
		label="Last_name",
		required = True,
		max_length=50,
		widget=forms.TextInput(attrs={
			'placeholder': 'Петренко',
			'class': 'form-control',
			'name': 'last_name'
			}))

	email = forms.EmailField(
		label="Email",
		required = True,
		max_length=50, 
		widget=forms.TextInput(attrs={
			'placeholder': 'pro100hacker@mail.com',
			'class': 'form-control',
			'name': 'email'
			}))

	password1 = forms.CharField(
		label="Password",
		help_text = '''
			Your password can't be too similar to your other personal information.<br/>
			Your password must contain at least 8 characters.<br/>
			Your password can't be a commonly used password.<br/>
			Your password can't be entirely numeric.
		''',
		max_length=50, 
		widget=forms.PasswordInput(attrs={
			'placeholder': 'passw@rd',
			'class': 'form-control',
			'name': 'password'
			}))

	password2 = forms.CharField(
		label="Password confirmation",
		help_text = 'Please confirm password.',
		max_length=50, 
		widget=forms.PasswordInput(attrs={
			'placeholder': 're-enter_passw@rd',
			'class': 'form-control',
			'name': 'password'
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

