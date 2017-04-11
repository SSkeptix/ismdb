from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from account import models 
from account import tuples


class EditUser(forms.ModelForm):
	email = forms.EmailField(required = True)
	first_name = forms.CharField(required = True)
	last_name = forms.CharField(required = True)

	class Meta:
		model = models.User
		fields = (
			'username',
			'first_name',
			'last_name',
			'email',
			)



class EditStudent(forms.ModelForm):
	lang = forms.ChoiceField(choices = tuples.LANG.SELECT, label = 'English level', required = True, widget=forms.Select())
	github = forms.CharField(label = 'GitHub', required = False)
	#description = forms.CharField(label = 'Describe yourself', max_length=2000, widget=forms.TextInput({}))

	class Meta:
		model = models.Student
		fields = (
			'lang',
			'group',
			'github',
			'description',
			)



class Add_lang(forms.ModelForm):
	class Meta:
		model = models.Student_lang
		exclude = (
			'validate_by', 
			'validate_at',
			)

	def save(self, commit=True):
		student = super(Add_lang, self).save(commit=False)

		student.skill = self.cleaned_data['skill']

		if commit:
			student.save()

		return student



class Add_fram(forms.ModelForm):
	class Meta:
		model = models.Student_fram
		exclude = (
			'validate_by', 
			'validate_at',
			)

	def save(self, commit=True):
		student = super(Add_fram, self).save(commit=False)

		student.lang = self.cleaned_data['lang']
		student.skill = self.cleaned_data['skill']

		if commit:
			student.save()

		return student


class Add_other(forms.ModelForm):
	class Meta:
		model = models.Student_other
		exclude = (
			'validate_by', 
			'validate_at',
			)

	def save(self, commit=True):
		student = super(Add_other, self).save(commit=False)

		student.skill = self.cleaned_data['skill']

		if commit:
			student.save()

		return student


