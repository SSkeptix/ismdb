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
			'style': 'width:auto;'
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
			'style': 'width:auto;'
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
			'style': 'width:auto;'
			}))

	class Meta:
		fields = ('value')


class Student:
	name = ''
	skills = []
	lang = ''

	def __init__(self, student):
		self.name = ('%s %s' % (student.user.last_name, student.user.first_name))
		self.lang = tuples.LANG().value(student.lang)
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