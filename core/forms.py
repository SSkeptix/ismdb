from django import forms
from account import models 
from account import tuples




class Lang(forms.Form):
	value = forms.ModelChoiceField(
		queryset = models.Language.objects.exclude(validated_by__isnull=True),
		label = 'Language',
		required = True,
		widget=forms.Select(attrs={
			'class': 'form-control',
			#'style': 'width:auto;'
			}))

	class Meta:
		fields = ('value')

class Fram(forms.Form):
	value = forms.ModelChoiceField(
		queryset = models.Framework.objects.exclude(validated_by__isnull=True),
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
		queryset = models.Other.objects.exclude(validated_by__isnull=True),
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
		choices = tuples.LANG.SELECT,
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
	lang = ''

	def __init__(self, student):
		self.name = ('{0} {1}'.format(student.user.last_name, student.user.first_name))
		self.lang = tuples.LANG().value(student.lang)
		self.username = student.user.username
		self.skills = []

		skills_queryset = models.Student_lang.objects.filter(student = student.user.id)
		for i in skills_queryset:
			self.skills.append(i.skill.value)

		skills_queryset = models.Student_fram.objects.filter(student = student.user.id)
		for i in skills_queryset:
			self.skills.append(i.skill.value)

		skills_queryset = models.Student_other.objects.filter(student = student.user.id)
		for i in skills_queryset:
			self.skills.append(i.skill.value)

		self.skills.sort()
