from django import forms
from account import models 
from account import tuples



'''
class Language(forms.Form):
	value = forms.ModelChoiceField(
		queryset = models.Language.objects.exclude(validated_by__isnull=True).order_by('value'),
		label = 'Language',
		required = True,
		widget=forms.Select(attrs={
			'class': 'form-control',
			#'style': 'width:auto;'
			}))

	class Meta:
		fields = ('value')

class Framework(forms.Form):
	value = forms.ModelChoiceField(
		queryset = models.Framework.objects.exclude(validated_by__isnull=True).order_by('lang__value', 'value'),
		label = 'Framework',
		required = True,
		widget=forms.Select(attrs={
			'class': 'form-control',
			#'style': 'width:auto;'
			}))

	class Meta:
		fields = ('value')

class Other(forms.Form):
	value = forms.ModelChoiceField(
		queryset = models.Other.objects.exclude(validated_by__isnull=True).order_by('value'),
		label = 'Other skill',
		required = True,
		widget=forms.Select(attrs={
			'class': 'form-control',
			#'style': 'width:auto;'
			}))

	class Meta:
		fields = ('value')



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



class Student:
	name = ''
	username = ''
	skills = []
	english = ''

	def __init__(self, student):
		self.name = ('{0} {1}'.format(student.user.last_name, student.user.first_name))
		self.english = tuples.ENGLISH().value(student.english)
		self.username = student.user.username
		self.skills = []

		skills_queryset = models.StudentLanguage.objects.filter(student = student.user.id)
		for i in skills_queryset:
			self.skills.append(i.skill.value)

		skills_queryset = models.StudentFramework.objects.filter(student = student.user.id)
		for i in skills_queryset:
			self.skills.append(i.skill.value)

		skills_queryset = models.StudentOther.objects.filter(student = student.user.id)
		for i in skills_queryset:
			self.skills.append(i.skill.value)

		self.skills.sort()
'''