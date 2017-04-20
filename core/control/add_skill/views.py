from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from account import models
from . import forms
from account import tuples

from itertools import chain

from django.http import HttpResponse



class AddSkill(TemplateView):
	template_name = 'core/add_skill.html'



	def get(self, request):
		if request.user.category in (tuples.CATEGORY.TEACHER, tuples.CATEGORY.EMPLOYER):
			permission = True
		else:
			permission = False


		# show skills that are waiting to confirmation
		skills = []

		queryset = models.Language.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, category='langs'))
		queryset = models.Framework.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, category='frams'))
		queryset = models.Other.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, category='others'))

		skills.sort(key=lambda instance: instance.added_at)


		args = {
			'lang_form': forms.Lang(),
			'fram_form': forms.Fram(),
			'other_form': forms.Other(),
			'permission': permission,
			'skills': skills,
		}

		return render(request, self.template_name, args)



	def post(self, request):
		args = {}

		if 'skills' in request.POST:

			if 'langs' in request.POST:
				skill = models.Language.objects.get(id = int(request.POST['langs']))
			elif 'frams' in request.POST:
				skill = models.Framework.objects.get(id = int(request.POST['frams']))
			elif 'others' in request.POST:
				skill = models.Other.objects.get(id = int(request.POST['others']))

			if request.POST['skills'] == 'Delete':
				skill.delete()
			elif request.POST['skills'] == 'Change':
				return HttpResponse('change')
			elif request.POST['skills'] == 'Save':
				skill.validated_by = models.User.objects.get(id=request.user.id)
				skill.save()

			return redirect('core:add_skill')

		else:
			if 'lang' in request.POST:
				form = forms.Lang(request.POST)
			elif 'fram' in request.POST:
				form = forms.Fram(request.POST)
			elif 'other' in request.POST:
				form = forms.Other(request.POST)

			if form.is_valid():
				if request.user.category in (tuples.CATEGORY.TEACHER, tuples.CATEGORY.EMPLOYER):
					form.save(validated_by = models.User.objects.get(id=request.user.id))
				else:
					form.save()
				return HttpResponse('saved')
				return redirect('core:add_skill')


		return render(request, self.template_name, args)


