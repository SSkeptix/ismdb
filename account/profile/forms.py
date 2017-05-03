from django import forms
from account import models 
from account import tuples
from .edit_forms import EditStudent

_class = 'form-control'





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
		required = True,
		widget=forms.CheckboxSelectMultiple()
		)


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


	def is_valid(self):
		valid = super(StudentSkill, self).is_valid()
		if not valid:
			return valid
		if models.StudentLanguage.objects.filter(student = self.student.user.id, skill = self.cleaned_data['skill']).count():
			self._errors['skill_exists'] = 'Skill is already exist'
			return False
		return True


	def __init__(self, *args, **kwargs):
		self.student = kwargs.pop('student', None)
		super(StudentSkill, self).__init__(*args, **kwargs)


	def save(self, commit=True):
		instance = super(StudentSkill, self).save(commit=False)
		instance.student = self.student

		if commit:
			instance.save()
		return instance