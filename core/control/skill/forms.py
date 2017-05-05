from django import forms
from account import models 

_style = ''
_class = 'form-control'



class Skill(forms.ModelForm):
	value = forms.CharField(
		label="Вміння",
		max_length=50,
		required = True,
		widget=forms.TextInput(attrs={
			'placeholder': 'Назва вміння',
			'class': _class,
			'style': _style,
			}))


	class Meta:
		model = models.Skill
		fields = ('value', )

	
	def save(self, commit=True, validated_by = None):
		instance = super(Skill, self).save(commit=False)

		if validated_by:
			instance.validated_by = validated_by

		if commit:
			instance.save()
		return instance





class SkillView:
	def __init__(self, skill):
		self.value = '<{0}>'.format(skill.__str__())
		self.id = skill.id
		self.date = skill.validated_at
