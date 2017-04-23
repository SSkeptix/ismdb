from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from account import models
from . import forms
from itertools import chain
import math


class Search(TemplateView):
	template_name = 'core/search.html'

	page = None
	rows = None
	languages = None
	frameworks = None
	others = None
	english = None



	def init(self, request, page):
		self.page = int(page)

		# number of rows per page in table results
		self.rows = 10

		# get filter data from url
		self.languages = request.GET.get('langs', None)
		self.frameworks = request.GET.get('frams', None)
		self.others = request.GET.get('others', None)
		self.english = request.GET.get('english', '1')



	def get(self, request, page = 1):
		self.init(request=request, page=page)
		args = {}

		# add filters
		kwargs_filter = {}

		if self.languages:
			for i in self.languages.split(","):
				kwargs_filter['StudentLanguage__skill'] = int (i)
		if self.frameworks:
			for i in self.frameworks.split(","):
				kwargs_filter['StudentFramework__skill'] = int (i)
		if self.others:
			for i in self.others.split(","):
				kwargs_filter['StudentOther__skill'] = int (i)
		kwargs_filter['english__gte'] = self.english

		# which data need get from database
		args_only = {
			'user',
			'english',
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
		students_count = models.Student.objects.filter(**kwargs_filter
			).select_related('user'
			).only(*args_only
			).order_by(*args_order_by
			).count()

		# args['page_range'] - number of result's pages = [1, 2, 3, 4, 5] - 5 pages
		args['page_range'] = []
		for i in range(1, 1 + math.ceil(students_count/self.rows)):
			args['page_range'].append(i)

		# take queryset (rows depends on 'page' and 'rows' - number of lines per page)
		students = models.Student.objects.filter(**kwargs_filter
			).select_related('user'
			).only(*args_only
			).order_by(*args_order_by
			)[
				(self.page-1)*self.rows : self.page*self.rows
			]

		# build list of student which include:
		# name, username, skills[], lang
		students_form = []
		for student in students:
			students_form.append(forms.Student(student = student))

		args['students'] = students_form

		args['language_form'] = forms.Language()
		args['framework_form'] = forms.Framework()
		args['other_form'] = forms.Other()
		args['english_form'] = forms.English(initial={'value': int(english)})
		args['page'] = self.page


		return render(request, self.template_name, args)



	def post(request, page):

		# !!!!!!!!!!!!!!
		# not fancy code --- but it work :)
		# send filter data to url
		url_data = '?'
		skill = [self.languages, self.frameworks, self.others]
		template = ['langs', 'frams', 'others']

		for i in range(0,3):
			if template[i] in request.POST:
				if i==0:
					form = forms.Language(request.POST)
				elif i==1:
					form = forms.Framework(request.POST)
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

		if 'english' in request.POST:
			form = forms.English(request.POST)
			if form.is_valid():
				var = form.cleaned_data['value']
				url_data += '{0}={1}&'.format('english', str(var))
		else:
			url_data += '{0}={1}&'.format('english', english)


		return redirect(reverse('core:search_page', kwargs={'page': 1}) + url_data)
