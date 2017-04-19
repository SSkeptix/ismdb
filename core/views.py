from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from account import models
from . import forms
from itertools import chain
import math

from django.http import HttpResponse


def search(request, page = 1):
	args = {}
	page = int(page)

	# number of rows per page in table results
	rows = 10

	#get filter data from url
	langs = request.GET.get('langs', None)
	frams = request.GET.get('frams', None)
	others = request.GET.get('others', None)
	english = request.GET.get('english', '1')

	#add filters
	kwargs_filter = {}

	if langs:
		for i in langs.split(","):
			kwargs_filter['student_lang__skill'] = int (i)
	if frams:
		for i in frams.split(","):
			kwargs_filter['student_fram__skill'] = int (i)
	if others:
		for i in others.split(","):
			kwargs_filter['student_other__skill'] = int (i)
	kwargs_filter['lang__gte'] = english

	# which data need get from database
	args_only = {
		'user',
		'lang',
		'user__id',
		'user__first_name',
		'user__last_name',
		'user__username'
	}

	# last parameter is primary in sorting
	args_order_by = {
		'user__first_name',	# second
		'user__last_name',	# first
	}

	# take number of all suitable students
	students_count = models.Student.objects.filter(**kwargs_filter).select_related('user').only(*args_only).order_by(*args_order_by).count()
	# args['page_range'] - number of result's pages = [1, 2, 3, 4, 5] - 5 pages
	args['page_range'] = []
	for i in range(1, 1 + math.ceil(students_count/rows)):
		args['page_range'].append(i)

	# take queryset (rows depends on 'page' and 'rows' - number of lines per page)
	students = models.Student.objects.filter(**kwargs_filter).select_related('user').only(*args_only).order_by(*args_order_by)[(page-1)*rows:page*rows]


	# build list of student which include:
	# name, username, skills[], lang
	students_form = []
	for student in students:
		students_form.append(forms.Student(student = student))

	args['students'] = students_form


	# !!!!!!!!!!!!!!
	# not fancy code --- but it work :)
	# send filter data to url
	url_data = '?'
	skill = [langs, frams, others]
	template = ['langs', 'frams', 'others']

	for i in range(0,3):
		if request.method == 'POST' and template[i] in request.POST:
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
			url_data += '{0}={1}&'.format(template[i], skill[i])

		elif skill[i]:
			url_data += '{0}={1}&'.format(template[i], skill[i])

	if request.method == 'POST' and 'english' in request.POST:
		form = forms.English(request.POST)
		if form.is_valid():
			var = form.cleaned_data['value']
			url_data += '{0}={1}&'.format('english', str(var))
	else:
		url_data += '{0}={1}&'.format('english', english)

	args['url_data'] = url_data

	if request.method == 'POST':
		return redirect(reverse('core:search_page', kwargs={'page': 1}) + url_data)


	args['lang_form'] = forms.Lang()
	args['fram_form'] = forms.Fram()
	args['other_form'] = forms.Other()
	args['english_form'] = forms.English(initial={'value': int(english)})
	args['page'] = page


	return render(request, 'core/search.html', args)



def add_skill(request):
	pass







def test(request):
	return render(request, 'core/test.html')