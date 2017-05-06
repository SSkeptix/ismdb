from django import forms
from account import models 
from account import tuples

_class = 'form-control'





class EditUser(forms.ModelForm):
	username = forms.CharField(
		label="Логін",
		help_text = '50 символів або менше, використовувати можна латинські букви, цифри і наступні символи: @/./+/-/_',
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
		if models.User.objects.exclude(id=self.instance.id).filter(email=self.cleaned_data['email']).exists():
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
			'placeholder': 'КН-32',
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





class AddStudent(EditStudent):
	user = None

	class Meta:
		model = models.Student
		fields = (
			'english',
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





class AddSkill(forms.Form):
	skill = forms.ModelMultipleChoiceField(
		queryset = models.Skill.objects.exclude(validated_by__isnull=True).order_by('value'),
		label = 'Вміння',
		required = False,
		widget=forms.CheckboxSelectMultiple()
		)


	def __init__(self, *args, **kwargs):
		self.user = kwargs.pop('user', None)
		super(AddSkill, self).__init__(*args, **kwargs)


	def save(self, commit=True):
		for skill in self.cleaned_data['skill']:
			models.StudentSkill(student_id = self.user.id, skill_id = skill.id).save()





class EditSkill(AddSkill):

	def __init__(self, *args, **kwargs):
		super(EditSkill, self).__init__(*args, **kwargs)
		
		self.initial_data = models.StudentSkill.objects.filter(student_id = self.user.id).values_list('skill', flat=True)
		self.fields['skill'].initial = self.initial_data



	def save(self, commit=True):
		data = []
		for skill in self.cleaned_data['skill']:
			data.append(skill.id)

		delete_skills = list(set(self.initial_data) - set(data))
		add_skills = list(set(data) - set(self.initial_data))

		print (delete_skills , '\n', add_skills)
		for i in delete_skills:
			models.StudentSkill.objects.get(student_id = self.user.id, skill_id = i).delete()

		for i in add_skills:
			models.StudentSkill(student_id = self.user.id, skill_id = i).save()





class StudentSkill(forms.ModelForm):
	student = None
	skill = forms.ModelChoiceField(
		queryset = models.Skill.objects.exclude(validated_by__isnull=True).order_by('value'),
		label = 'Вміння',
		required = True,
		widget=forms.Select(attrs={
			'class': _class,
			'style': 'width:auto;'
			}))


	class Meta:
		model = models.StudentSkill
		exclude = (
			'student',
			'validated_by', 
			'validated_at',
			)


	def __init__(self, *args, **kwargs):
		self.student = kwargs.pop('student', None)
		super(StudentSkill, self).__init__(*args, **kwargs)


	def is_valid(self):
		valid = super(StudentSkill, self).is_valid()
		if not valid:
			return valid
		if models.StudentSkill.objects.filter(student = self.student.user.id, skill = self.cleaned_data['skill']).count():
			self._errors['skill_exists'] = 'Skill is already exist'
			return False
		return True


	def save(self, commit=True):
		instance = super(StudentSkill, self).save(commit=False)
		instance.student = self.student

		if commit:
			instance.save()
		return instance