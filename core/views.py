from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from account import models

from . import forms
#from . import tuples

from itertools import chain

from django.http import HttpResponse


# Create your views here.
def search(request, page = 1):

	#get filter data from url
	langs = request.GET.get('langs', None)
	frams = request.GET.get('frams', None)
	others = request.GET.get('others', None)

	args = {
		'lang_form': forms.Lang(),
		'fram_form': forms.Fram(),
		'other_form': forms.Other(),
		'page': page,
	}

	#add filters
	kwargs_filter = {}

	if langs:
		filter_langs = []
		for i in langs.split(","):
			filter_langs.append(int (i))
		kwargs_filter['student_lang__skill__in'] = filter_langs

	if frams:
		filter_frams = []
		for i in frams.split(","):
			filter_frams.append(int (i))
		kwargs_filter['student_fram__skill__in'] = filter_frams

	if others:
		filter_others = []
		for i in others.split(","):
			filter_others.append(int (i))
		kwargs_filter['student_other__skill__in'] = filter_others

	english = request.GET.get('english', None)
	if english:
		kwargs_filter['lang__gte'] = english

	args_only = {
		'user',
		'lang',
		'user__id',
		'user__first_name',
		'user__last_name'
	}

	# last parameter is primary in sorting
	args_order_by = {
		'user__first_name',	# second
		'user__last_name',	# first
	}


	# take queryset
	students = models.Student.objects.filter(**kwargs_filter).select_related('user').only(*args_only).order_by(*args_order_by).distinct()


	# build list of student which include:
	# name, skills[], lang
	students_form = []
	for student in students:
		students_form.append(forms.Student(student = student))

	args['students'] = students_form


	# !!!!!!!!!!!!!!
	# not fancy code --- but it work :)
	# send filter data to url
	if request.method == 'POST':
		base_url = reverse('core:search_filter', kwargs={'page': 1}) + '?'

		skill = [langs, frams, others]
		template = ['langs', 'frams', 'others']
		for i in range(0,3):
			if template[i] in request.POST:
				if i==0:
					form = forms.Lang(request.POST)
				elif i==1:
					form = forms.Fram(request.POST)
				elif i==2:
					form = forms.Other(request.POST)

				if form.is_valid():
					var = form.cleaned_data['value'].id
				if skill[i]:
					if not (str(var) in skill[i]):
						skill[i] += (',{0}'.format(str(var)))
				else:
					skill[i] = str(var)
				base_url += '{0}={1}&'.format(template[i], skill[i])

			elif skill[i]:
				base_url += '{0}={1}&'.format(template[i], skill[i])

		return redirect(base_url)



	return render(request, 'core/search.html', args)

