from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView
from account import tuples
from account import models

from . import forms
from . import edit_forms
from . import view_forms

from django.http import HttpResponse

#reverse('account:add_skill', kwargs={'username': request.user.username})





def add_profile(request):
	args = {}

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



	def render(self, request, username = '', new_args = None):
		args = {}
		user = models.User.objects.get(username = request.user.username)
		profile = models.User.objects.get(username = username)
		args['user_form'] = profile

		# validation permission - possibility to validate:
		# student's skill, persons
		if (user.category == tuples.CATEGORY.TEACHER) and user.validated_by:
			validation_permission = True
			if (username == user.username) :
				validation_permission = False
		else:
			validation_permission = False
		args['validation_permission'] = validation_permission


		if (username == user.username) :
			own_profile = True
		else:
			own_profile = False
		args['own_profile'] = own_profile

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
		if (request.user.category == tuples.CATEGORY.STUDENT) :
			student = models.Student.objects.get(user = request.user.id)

		# show skills
			skills = []
			for i in models.StudentSkill.objects.filter(student = student.user.id):
				skills.append(view_forms.Skill(skill=i))

			skills.sort(key=lambda instance: instance.value)

			args = {
				'skills': skills,
				'user_form': edit_forms.EditUser(instance = request.user),
				'student_form': edit_forms.EditStudent(instance = student),
			}
		else:
		# edit profile (teacher, employer)
			args = {
				'user_form': edit_forms.EditUser(instance = request.user),
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
			if 'profile' in request.POST:
				student = models.Student.objects.get(user = request.user.id)
				user_form = edit_forms.EditUser(request.POST, instance = request.user)
				student_form = edit_forms.EditStudent(request.POST, instance = student)
				if user_form.is_valid() and student_form.is_valid():
					user_form.save()
					student_form.save()
					return redirect('account:profile', username=request.user.username)
				else:
					args = {
						'user_form': user_form,
						'student_form':student_form,
					}
					return self.render(request=request, username=username, new_args=args)
		
		# delete skill
			elif 'skill' in request.POST:
				models.StudentSkill.objects.get(id = int(request.POST['skill'])).delete()

		else:
		# edit profile (teacher, employer)
			if 'profile' in request.POST:
				user_form = edit_forms.EditUser(request.POST, instance = request.user)
				if user_form.is_valid():
					user_form.save()
					return redirect('account:profile', username=request.user.username)
				else:
					args = {'user_form': user_form, }
					return self.render(request=request, username=username, new_args=args)

		return self.get(request=request, username=username)




'''
class AddSkill(TemplateView):
	template_name = 'account/profile/add_skill.html'



	def render(self, request, username = '', new_args = None):
		args = {
			'skill_form': forms.StudentSkill(),
			'framework_form': forms.StudentFramework(),
			'other_form': forms.StudentOther(),
		}

		if new_args:
			for i in new_args:
				args[i] = new_args[i]
		return render(request, self.template_name, args)



	def get(self, request, username = ''):
		if username != request.user.username:
			return redirect('account:add_skill', username=request.user.username)

		#if student profile don't exist create profile
		if models.Student.objects.filter(user = request.user.id).exists() :
			student = models.Student.objects.get(user = request.user.id)
		else:
			return redirect('account:add_profile')

		return self.render(request=request, username=username)



	def post(self, request, username = ''):
		student = models.Student.objects.get(user = request.user.id)

		if 'language' in request.POST:
			form = forms.StudentLanguage(request.POST, student=student)
		elif 'framework' in request.POST:
			form = forms.StudentFramework(request.POST, student=student)
		elif 'other' in request.POST:
			form = forms.StudentOther(request.POST, student=student)	

		if form.is_valid():
			form.save()
			return redirect('account:add_skill', username=request.user.username)
		else:

			if 'language' in request.POST:
				args = {'language_form': form, }
			elif 'framework' in request.POST:
				args = {'framework_form': form, }
			elif 'other' in request.POST:
				args = {'other_form': form, }
			
			return self.render(request=request, username=username, new_args=args)
		
		return self.get(request=request, username=username)

'''