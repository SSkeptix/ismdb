from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from account import models

from . import forms
#from . import tuples

from itertools import chain

from django.http import HttpResponse


# Create your views here.
def search(request, filter_langs = None, filter_frams = None, filter_others = None):

	args = {}

	args['add_lang'] = forms.Lang()

	filter_langs = 2

	#Entry.objects.filter(id__gt=4)


# get queryset
	if filter_langs:
		kwargs = {'show': True, 'skill': filter_langs}
		langs = models.Student_lang.objects.filter(skill_id = 2)

	else:
		langs = models.Student_lang.objects.filter(show=True)


	if filter_frams:
		frams = models.Student_fram.objects.filter(show=True, skill = filter_frams)
	else:
		frams = models.Student_fram.objects.filter(show=True)

	if filter_others:
		others = models.Student_other.objects.filter(show=True, skill = filter_others)
	else:
		others = models.Student_other.objects.filter(show=True)

	if langs or frams or others:
		skills = sorted(
				chain(langs),#, frams, others),
				key=lambda instance: (instance.skill.__str__())
				)
	else:
		skills = False






	args['skills'] = skills


	return render(request, 'core/search.html', args)

