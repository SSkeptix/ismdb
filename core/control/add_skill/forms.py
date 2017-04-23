from django import forms
from account import models 

_style = 'width:auto;'
_class = 'form-control'





# base form for all type of skill
class Skill(forms.ModelForm):
	def save(self, commit=True, validated_by = None):
		instance = super(Skill, self).save(commit=False)

		if validated_by:
			instance.validated_by = validated_by

		if commit:
			instance.save()
		return instance





class Language(Skill):
	value = forms.CharField(
		label="Language",
		max_length=50,
		required = True,
		widget=forms.TextInput(attrs={
			'placeholder': 'Title of language',
			'class': _class,
			'style': _style,
			}))

	class Meta:
		model = models.Language
		fields = ('value', )





class Framework(Skill):
	lang = forms.ModelChoiceField(
		queryset = models.Language.objects.exclude(validated_by__isnull=True).order_by('value'),
		label = 'Language',
		required = True,
		widget=forms.Select(attrs={
			'class': _class,
			'style': _style,
			}))

	value = forms.CharField(
		label="Framework",
		max_length=50,
		required = True,
		widget=forms.TextInput(attrs={
			'placeholder': 'Title of framework',
			'class': _class,
			'style': _style,
			}))

	class Meta:
		model = models.Framework
		fields = ('lang', 'value', )



class Other(Skill):
	value = forms.CharField(
		label="Other",
		max_length=50,
		required = True,
		widget=forms.TextInput(attrs={
			'placeholder': 'Title of technique',
			'class': _class,
			'style': _style,
			}))

	class Meta:
		model = models.Other
		fields = ('value', )





# for 'edit_profile' and 'profile'
class SkillView:
	category = None
	value = None
	id = None
	added_at = None

	def __init__(self, skill, category):
		self.category = category
		self.value = '<{0}>'.format(skill.__str__())
		self.id = skill.id
		self.added_at = skill.validated_at

