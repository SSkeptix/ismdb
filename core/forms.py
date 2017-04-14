from django import forms
from django.db.models import Q

from account import models 
from account import tuples




class Lang(forms.Form):
	value = forms.ModelChoiceField(
		queryset = models.Language.objects.exclude(validated_by__isnull=True),
		label = 'Languages',
		required = True,
		widget=forms.Select(attrs={
			'class': 'form-control',
			'style': 'width:auto;'
			}))

	class Meta:
		fields = ('value')


