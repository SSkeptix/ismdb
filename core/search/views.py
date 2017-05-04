from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from account import models
from . import forms
from itertools import chain
import math




class Search(TemplateView):
	template_name = 'core/search/search.html'

	page = None
	rows = None
	skills = None
	english = None



	def init(self, request, page):
		self.page = int(page)

		# number of rows per page in table results
		self.rows = 10

		# get filter data from url
		self.skills = request.GET.get('skills', None)
		self.english = request.GET.get('english', '1')



	def get(self, request, page = 1):
		self.init(request=request, page=page)
		args = {}

		# add filters
		kwargs_filter = {}

		initial_skill = []
		if self.skills:
			for i in self.skills.split(","):
				initial_skill.append(int (i))
				kwargs_filter['studentskill__skill'] = int (i)

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
		# name, username, skills[], english
		students_form = []
		for student in students:
			students_form.append(forms.Student(student = student))

		url_data = '?skills={0}&english={1}'.format(self.skills, self.english)
		args['url_data'] = url_data



		args['students'] = students_form
		args['skill_form'] = forms.Skill(initial={'skill': initial_skill})
		args['english_form'] = forms.English(initial={'value': self.english})
		args['page'] = self.page
		

		print(kwargs_filter)
		return render(request, self.template_name, args)



	def post(self, request, page = 1):
		self.init(request=request, page=page)

		# send filter data to url
		url_data = '?'

		skill_form = forms.Skill(request.POST)
		english_form = forms.English(request.POST)
		if skill_form.is_valid() and english_form.is_valid():
			skill = skill_form.get_list()
			if skill:
				url_data +='skills='
				for i in skill:
					url_data +='{0},'.format(str(i))
				url_data = url_data[:-1] + '&'

			english = english_form.cleaned_data['value']
			url_data += '{0}={1}&'.format('english', str(english))

		return redirect(reverse('core:search_page', kwargs={'page': 1}) + url_data)
