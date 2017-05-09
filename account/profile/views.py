from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from account import tuples
from account import models

from . import forms
from . import view_forms

from django.http import Http404, HttpResponse

from core.functions import validation_permission





def add_profile(request):
	if (request.user.category != tuples.CATEGORY.STUDENT or 
		models.Student.objects.filter(user_id = request.user.id).exists()
		):
		return redirect('404')


	args = {'validation_permission': validation_permission(user=request.user), }

	# add student profile
	if request.method == 'POST' :
		form = forms.AddStudent(request.POST, user=request.user)
		skill_form = forms.AddSkill(request.POST, user=request.user)
		if form.is_valid() and skill_form.is_valid():
			form.save()
			skill_form.save()

			return redirect('account:profile', username=request.user.username)
	else:
		form = forms.AddStudent()
		skill_form = forms.AddSkill()

	args = {
		'form': form,
		'skill_form': skill_form,
	}

	return render(request, 'account/profile/add_profile.html', args)





# Show own or someone else's profile
class Profile(TemplateView):
	template_name = 'account/profile/profile.html'



	def render(self, request, username, new_args = None):
		args = {'validation_permission': validation_permission(user=request.user), }
		
		args['own_profile'] = False
		if request.user.is_authenticated and username == request.user.username :
			args['own_profile'] = True


		profile = models.User.objects.get(username = username)
		args['user_form'] = profile
		args['user_category'] = tuples.CATEGORY().value(profile.category) 

		# validation permission - possibility to validate:
		# student's skill, persons
		




		# if user want to view profile of student
		if (profile.category == tuples.CATEGORY.STUDENT) and models.Student.objects.filter(user = profile.id).exists() :
			student = models.Student.objects.get(user = profile.id)
			args['student'] = student
			args['student_english'] = tuples.ENGLISH().value(student.english)

		# show skills
			skills = []
			for i in models.StudentSkill.objects.filter(student = student.user.id):
				skills.append(view_forms.Skill(skill=i))

			skills.sort(key=lambda instance: instance.value)
			args['skills'] = skills


		if new_args:
			for i in new_args:
				args[i] = new_args[i]
		return render(request, self.template_name, args)



	def get(self, request, username = ''):
		if username == '':
			return redirect('account:profile', username=request.user.username)

		#if student profile don't exist create profile
		if (
			request.user.is_authenticated and
			username == request.user.username and
			request.user.category == tuples.CATEGORY.STUDENT and 
			models.Student.objects.filter(user = request.user.id).exists() == False
			):
			return redirect('account:add_profile')

		return self.render(request=request, username=username)



	def post(self, request, username = ''):

		if 'skill_validation' in request.POST:
			skill = models.StudentSkill.objects.get(id = int(request.POST['id']))

			skill.validated_by = models.User.objects.only('id').get(username = request.user.username)
			skill.save()
			return redirect('account:profile', username = username)

		elif 'user_validation' in request.POST:
			profile = models.User.objects.get(username = username)
			profile.validated_by = models.User.objects.only('id').get(username = request.user.username)
			profile.save()
			return redirect ('account:profile', username=profile.username)

		return self.get(request=request, username=username)






class EditProfile(TemplateView):
	template_name = 'account/profile/edit.html'



	def render(self, request, username = '', new_args = None):
		args = {'validation_permission': validation_permission(user=request.user), }

		if (request.user.category == tuples.CATEGORY.STUDENT) :
			student = models.Student.objects.get(user = request.user.id)

			args['user_form'] = forms.EditUser(instance = request.user)
			args['student_form'] = forms.EditStudent(instance = student)
			args['skill_form'] = forms.EditSkill(user = request.user)
			
		else:
		# edit profile (teacher, employer)
			args = {
				'user_form': forms.EditUser(instance = request.user),
			}
			
		if new_args:
			for i in new_args:
				args[i] = new_args[i]
		return render(request, self.template_name, args)



	def get(self, request, username = ''):
		if username != request.user.username:
			return redirect('account:edit_profile', username=request.user.username)

		#if student profile don't exist create profile
		if (
			request.user.category == tuples.CATEGORY.STUDENT and 
			models.Student.objects.filter(user = request.user.id).exists() == False
			):
			return redirect('account:add_profile')

		return self.render(request=request, username=username)



	def post(self, request, username = ''):
		if (request.user.category == tuples.CATEGORY.STUDENT) :

		# edit student profile
			student = models.Student.objects.get(user = request.user.id)
			user_form = forms.EditUser(request.POST, instance = request.user)
			student_form = forms.EditStudent(request.POST, instance = student)
			skill_form = forms.EditSkill(request.POST, user = request.user)
			if user_form.is_valid() and student_form.is_valid() and skill_form.is_valid():
				user_form.save()
				student_form.save()
				skill_form.save()
				return redirect('account:profile', username=request.user.username)
			else:
				args = {
					'user_form': user_form,
					'student_form':student_form,
					'skill_form': skill_form,
				}
				return self.render(request=request, username=username, new_args=args)

		else:
		# edit profile (teacher, employer)
			user_form = forms.EditUser(request.POST, instance = request.user)
			if user_form.is_valid():
				user_form.save()
				return redirect('account:profile', username=request.user.username)
			else:
				args = {'user_form': user_form, }
				return self.render(request=request, username=username, new_args=args)

		return self.get(request=request, username=username)