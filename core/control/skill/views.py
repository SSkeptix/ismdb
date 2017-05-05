from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from account import models
from account import tuples
from . import forms
from django.http import Http404, HttpResponse

from itertools import chain





class AddSkill(TemplateView):
	template_name = 'core/control/add_skill.html'

	add_permission = None
	validation_permission = None



	def init(self, request):
		if request.user.validated_by:
			self.add_permission = True
			if request.user.category in (tuples.CATEGORY.TEACHER, tuples.CATEGORY.EMPLOYER):
				self.validation_permission = True
		else:
			self.add_permission = False
			self.validation_permission = False			



	def render(self, request, new_args = None):
		
		# show skills that are waiting to confirmation
		skills = []

		queryset = models.Skill.objects.filter(validated_by__isnull = True).order_by('value')
		for i in queryset:
			skills.append(forms.SkillView(skill=i))

		args = {
			'skill_form': forms.Skill(),
			'add_permission': self.add_permission,
			'validation_permission': self.validation_permission,
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
			skill = models.Skill.objects.get(id = int(request.POST['skill_id']))

			if request.POST['skill_validation'] == 'Видалити':
				skill.delete()
			elif request.POST['skill_validation'] == 'Змінити':
				return redirect('core:edit_skill', id=skill.id)
			elif request.POST['skill_validation'] == 'Зберегти':
				skill.validated_by = models.User.objects.get(id=request.user.id)
				skill.save()

			return redirect('core:add_skill')

		elif 'add_skill' in request.POST:
			form = forms.Skill(request.POST)

			if form.is_valid():
				if self.validation_permission:
					form.save(validated_by = models.User.objects.get(id=request.user.id))
				else:
					form.save()
				return redirect('core:add_skill')

			else:
				args = {'skill_form': form, }
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



	def get(self, request, id):
		id = int(id)

		skill = models.Skill.objects.get(id = id)
		form = forms.Skill(instance = skill)

		#skill is already validated
		if skill.validated_by:
			raise Http404('Ви не маєте прав на редагування цього вміння')	

		args = {'form': form, }

		return self.render(request=request, new_args=args)



	def post(self, request, id):
		form = forms.Skill(request.POST, instance = models.Skill.objects.get(id = id))

		if form.is_valid():
			form.save(validated_by = models.User.objects.get(id=request.user.id))
			return redirect('core:add_skill')
		else: 
			args = {'form': form, }
			return self.render(request=request, new_args=args)
