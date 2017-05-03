from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from account import models
from account import tuples
from . import forms
from django.http import Http404, HttpResponse

from itertools import chain

'''
# support class for writing short code
class SKILL:
	LANGUAGE = tuples.SKILL().value(tuples.SKILL.LANGUAGE)
	FRAMEWORK = tuples.SKILL().value(tuples.SKILL.FRAMEWORK)
	OTHER = tuples.SKILL().value(tuples.SKILL.OTHER)






class AddSkill(TemplateView):
	template_name = 'core/control/add_skill.html'

	permission = None



	def init(self, request):
		if request.user.category in (tuples.CATEGORY.TEACHER, tuples.CATEGORY.EMPLOYER) and request.user.validated_by:
			self.permission = True
		else:
			self.permission = False
		


	def render(self, request, new_args = None):
		

		# show skills that are waiting to confirmation
		skills = []

		queryset = models.Language.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, skill_type=SKILL.LANGUAGE))
		queryset = models.Framework.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, skill_type=SKILL.FRAMEWORK))
		queryset = models.Other.objects.filter(validated_by__isnull = True)
		for i in queryset:
			skills.append(forms.SkillView(skill=i, skill_type=SKILL.OTHER))

		skills.sort(key=lambda instance: instance.value)

		args = {
			'language_form': forms.Language(),
			'framework_form': forms.Framework(),
			'other_form': forms.Other(),
			'permission': self.permission,
			'skills': skills,
		}


		if new_args:
			for i in new_args:
				args[i] = new_args[i]
		return render(request, self.template_name, args)



	def get(self, request):
		self.init(request=request)

		return self.render(request=request)



	def post(self, request):
		self.init(request=request)

		if 'skill_validation' in request.POST:

			if SKILL.LANGUAGE in request.POST:
				skill = models.Language.objects.get(id = int(request.POST[SKILL.LANGUAGE]))
				skill_type = 'lang'
			elif SKILL.FRAMEWORK in request.POST:
				skill = models.Framework.objects.get(id = int(request.POST[SKILL.FRAMEWORK ]))
				skill_type = 'fram'
			elif SKILL.OTHER in request.POST:
				skill = models.Other.objects.get(id = int(request.POST[SKILL.OTHER]))
				skill_type = 'other'

			if request.POST['skill_validation'] == 'Delete':
				skill.delete()
			elif request.POST['skill_validation'] == 'Change':
				return redirect('core:edit_skill', id=skill.id, skill_type=skill_type)
			elif request.POST['skill_validation'] == 'Save':
				skill.validated_by = models.User.objects.get(id=request.user.id)
				skill.save()

			return redirect('core:add_skill')

		else:
			if 'add_language' in request.POST:
				form = forms.Language(request.POST)
			elif 'add_framework' in request.POST:
				form = forms.Framework(request.POST)
			elif 'add_other' in request.POST:
				form = forms.Other(request.POST)

			if form.is_valid():
				if self.permission:
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





class EditSkill(TemplateView):
	template_name = 'core/control/edit_skill.html'


	def render(self, request, new_args = None):
		args = {}

		if new_args:
			for i in new_args:
				args[i] = new_args[i]
		return render(request, self.template_name, args)


	def get(self, request, id, skill_type):
		id = int(id)

		if skill_type == 'lang':
			skill = models.Language.objects.get(id = id)
			form = forms.Language(instance = skill)

		elif skill_type == 'fram':
			skill = models.Framework.objects.get(id = id)
			form = forms.Framework(instance = skill)

		elif skill_type == 'other':
			skill = models.Other.objects.get(id = id)
			form = eforms.Other(instance = skill)


		#skill is already validated
		if skill.validated_by:
			raise Http404('You dont have permission to change this skill')	

		args = {'form': form, }

		return self.render(request=request, new_args=args)




	def post(self, request, id, skill_type):

		if SKILL.LANGUAGE in request.POST:
			form = forms.Language(request.POST, instance = models.Language.objects.get(id = id))
		elif SKILL.FRAMEWORK in request.POST:
			form = forms.Framework(request.POST, instance = models.Framework.objects.get(id = id))
		if SKILL.OTHER in request.POST:
			form = forms.Other(request.POST, instance = models.Other.objects.get(id = id))


		if form.is_valid():
			form.save(validated_by = models.User.objects.get(id=request.user.id))
			return redirect('core:add_skill')
		else: 
			args = {'form': form, }
			return self.render(request=request, new_args=args)
'''