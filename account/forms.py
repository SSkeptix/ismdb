from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Student
from . import tuples

class Login(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30, 
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30, 
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class Registration(UserCreationForm):
	email = forms.EmailField(required = True)
	first_name = forms.CharField(required = True)
	last_name = forms.CharField(required = True)

	class Meta:
		model = User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			'password1',
			'password2',
			'group',
			)

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.group = self.cleaned_data['group']
		

		if commit:
			user.save()

		return user


'''
class RegistrationStudent(forms.ModelForm):
	lang = form.ChoiceField(choice = tuples.LANG.SELECT, default = tuples.LANG.A1)
	group = forms.CharField(required = True)
	gitHub = forms.URLField(required = False)
	describe = forms.TextField(required = False)


	class Meta:
		model = Student
		fields = (
			'lang',
			'group',
			'gitHub',
			'describe',
			)

	def save(self, commit=True):
		user = super(RegistrationForm, self).save(commit=False)
		user.first_name = self.cleaned_data['first_name']
		user.last_name = self.cleaned_data['last_name']
		user.email = self.cleaned_data['email']
		user.group = self.cleaned_data['group']
		

		if commit:
			user.save()

		return user





class Add_skill(forms.ModelForm):
	
    skill = forms.ModelChoiceField(queryset = Skill.objects.all())

    class Meta:
        model = Student_skill
        fields = ('skill',)
'''
