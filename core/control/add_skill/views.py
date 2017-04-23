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



	def render(self, request, new_args = None):
		if request.user.category in (tuples.CATEGORY.TEACHER, tuples.CATEGORY.EMPLOYER) and user.validated_by:
			permission = True
		else:
			permission = False

		# show skills that are waiting to confirmation
		skills = []

		queryset = models.Language.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, category='language'))
		queryset = models.Framework.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, category='framework'))
		queryset = models.Other.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, category='other'))

		skills.sort(key=lambda instance: instance.value)

		args = {
			'language_form': forms.Lang(),
			'framework_form': forms.Fram(),
			'other_form': forms.Other(),
			'permission': permission,
			'skills': skills,
		}


		if new_args:
			for i in new_args:
				args[i] = new_args[i]
		return render(request, self.template_name, args)



	def get(self, request):
		return self.render(request=request)



	def post(self, request):
		if 'skill_validation' in request.POST:

			if 'language' in request.POST:
				skill = models.Language.objects.get(id = int(request.POST['language']))
			elif 'framework' in request.POST:
				skill = models.Framework.objects.get(id = int(request.POST['framwork']))
			elif 'other' in request.POST:
				skill = models.Other.objects.get(id = int(request.POST['other']))

			if request.POST['skill_validation'] == 'Delete':
				skill.delete()
			elif request.POST['skill_validation'] == 'Change':
				return HttpResponse('change')
			elif request.POST['skill_validation'] == 'Save':
				skill.validated_by = models.User.objects.get(id=request.user.id)
				skill.save()

			return redirect('core:add_skill')

		else:
			if 'add_language' in request.POST:
				form = forms.Lang(request.POST)
			elif 'add_framework' in request.POST:
				form = forms.Fram(request.POST)
			elif 'add_other' in request.POST:
				form = forms.Other(request.POST)

			if form.is_valid():
				if request.user.category in (tuples.CATEGORY.TEACHER, tuples.CATEGORY.EMPLOYER):
					form.save(validated_by = models.User.objects.get(id=request.user.id))
				else:
					form.save()
				return redirect('core:add_skill')

			else:
				if 'add_language' in request.POST:
					args = {'language_form': form, }
				elif 'add_framework' in request.POST:
					args = {'framework_form': form, }
				elif 'add_other' in request.POST:
					args = {'other_form': form, }
				
				return self.render(request=request, new_args=args)

		return self.get(request=request)

