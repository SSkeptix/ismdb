from django import forms
from account import models 
from account import tuples




class Skill(forms.Form):
	skill = forms.ModelMultipleChoiceField(
		queryset = models.Skill.objects.exclude(validated_by__isnull=True).order_by('value'),
		label = 'Вміння',
		required = False,
		widget=forms.CheckboxSelectMultiple()
		)


	def get_list(self):
		data = []
		for skill in self.cleaned_data['skill']:
			data.append(skill.id)

		return data

			



class English(forms.Form):
	value = forms.ChoiceField(
		choices = tuples.ENGLISH.SELECT,
		label = 'English level',
		required = True,
		widget=forms.Select(attrs={
			'class': 'form-control',
			#'style': 'width:auto;'
			}))

	class Meta:
		fields = ('value')



class Validated(forms.Form):
	validated = forms.BooleanField(
		label = 'Лише перевірені студенти',
		required = False,
		widget = forms.CheckboxInput(attrs={
			'style': 'width:auto;display:block-inline;'
			}))




class Student:
	name = ''
	username = ''
	skills = []
	english = ''

	def __init__(self, student):
		self.name = student.user
		self.english = tuples.ENGLISH().value(student.english)
		self.username = student.user.username
		self.skills = ''

		skills_queryset = models.Skill.objects.filter(studentskill__student = student.user.id).order_by('value')
		if skills_queryset:
			for i in skills_queryset:
				self.skills += '{0}, '.format(i.value)
			self.skills = self.skills[:-2]
		else:
			self.skills = '-----'

		

