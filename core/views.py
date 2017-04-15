from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from account import models

from . import forms
#from . import tuples

from itertools import chain

from django.http import HttpResponse


# Create your views here.
def search(request, page = 1, langs = None, frams = None, others = None, english = None):

	args = {
		'lang_form': forms.Lang(),
		'page': page,
	}

	#add filters
	kwargs_filter = {}


	langs = request.GET.get('langs')
	if langs:
		filter_langs = []
		for i in langs.split(","):
			filter_langs.append(int (i))
		kwargs_filter['student_lang__skill__in'] = filter_langs

	frams = request.GET.get('frams')
	if frams:
		filter_frams = []
		for i in langs.split(","):
			filter_frams.append(int (i))
		kwargs_filter['student_fram__skill__in'] = frams

	others = request.GET.get('others')
	if others:
		filter_others = []
		for i in langs.split(","):
			filter_others.append(int (i))
		kwargs_filter['student_other__skill__in'] = filter_others

	english = request.GET.get('english')
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

	
	if request.method == 'POST' and 'add_lang' in request.POST:
		form = forms.Lang(request.POST)
		if form.is_valid():
			var = form.cleaned_data['value'].id
		else:
			var = 15
		base_url = reverse('core:search_filter', kwargs={'page': 1})
		
		if langs:
			if not (str(var) in langs):
				langs += (',{0}'.format(str(var)))
		else:
			langs = str(var)

		base_url += '?langs={0}'.format(langs)


		if frams:
			base_url += '?frams={0}'.format(frams)
		if others:
			base_url += '?others={0}'.format(others)
		if english:
			base_url += '?english={0}'.format(english)

		return redirect(base_url)
	

	#debuging information
	args['this_page'] = '{0}?{1}'.format(reverse('core:search_filter', kwargs={'page': 1}), 'langs=1,2,3')



	return render(request, 'core/search.html', args)

