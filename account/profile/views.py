from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from . import forms
from account import tuples
from account import models

from itertools import chain

from django.http import HttpResponse



@login_required(login_url="account:login")
def add_profile(request):

	args = {}

	# add student profile
	if request.method == 'POST' :
		form = forms.AddStudent(request.POST, user=request.user)
		if form.is_valid():
			form.save()
			return redirect('account:profile', username=request.user.username)
	else:
		form = forms.AddStudent()


	args['form'] = form

	return render(request, 'account/profile/add_profile.html', args)



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!! need add teacher validation featers
# Show own or someone else's profile
@login_required(login_url="account:login")
def profile(request, username = ''):
	if username == '':
		return redirect('account:profile', username=request.user.username)


	args = {}
	user = request.user
	profile = models.User.objects.get(username = username)
	if (user.category == tuples.CATEGORY.TEACHER) :
		is_teacher = True
		if (username == user.username) :
			is_teacher = False
	else:
		is_teacher = False

	if (username == user.username) :
		own_profile = True
	else:
		own_profile = False

	args['validation_permission'] = is_teacher
	args['own_profile'] = own_profile
	args['user'] = profile
	

	# if user want to view profile of student
	if (profile.category == tuples.CATEGORY.STUDENT) and models.Student.objects.filter(user = profile.id).exists() :
		student = models.StudentProfile.objects.get(user = profile.id)

		args['student'] = student
		args['student_lang'] = tuples.LANG().value(student.lang)


	# show skills
		skills = []

		langs = models.Student_lang.objects.filter(student = student.user.id)
		for skill in langs:
			skills.append(forms.SkillView(skill=skill, category='lang'))
		frams = models.Student_fram.objects.filter(student = student.user.id)
		for skill in frams:
			skills.append(forms.SkillView(skill=skill, category='fram'))
		others = models.Student_other.objects.filter(student = student.user.id)
		for skill in others:
			skills.append(forms.SkillView(skill=skill, category='other'))

		skills.sort(key=lambda instance: instance.value)
		args['skills'] = skills


	return render(request, 'account/profile/profile.html', args)



# Edit own profile
@login_required(login_url="account:login")
def edit_profile(request, username = ''):
	args = {}

	if (request.user.category == tuples.CATEGORY.STUDENT) :

	#if student profile don't exist create profile
		if models.StudentProfile.objects.filter(user = request.user.id).exists() :
			student = models.StudentProfile.objects.get(user = request.user.id)
		else:
			return redirect('account:add_profile')

	# delete skill
		if request.method == 'POST':
			if 'langs' in request.POST:
				models.Student_lang.objects.get(id = int(request.POST['langs'])).delete()
			if 'frams' in request.POST:
				models.Student_fram.objects.get(id = int(request.POST['frams'])).delete()
			if 'others' in request.POST:
				models.Student_other.objects.get(id = int(request.POST['others'])).delete()

	# edit student profile
		if request.method == 'POST' and 'profile' in request.POST:
			form = forms.EditUser(request.POST, instance = request.user)
			student_form = forms.EditStudent(request.POST, instance = student)
			if form.is_valid() and student_form.is_valid():
				form.save()
				student_form.save()
				return redirect('account:profile', username=request.user.username)
		else:
			form = forms.EditUser(instance = request.user)
			student_form = forms.EditStudent(instance = student)

		args['form'] = form
		args['student_form'] = student_form


	# show skills
		skills = []

		langs = models.Student_lang.objects.filter(student = student.user.id)
		for skill in langs:
			skills.append(forms.SkillView(skill=skill, category='langs'))
		frams = models.Student_fram.objects.filter(student = student.user.id)
		for skill in frams:
			skills.append(forms.SkillView(skill=skill, category='frams'))
		others = models.Student_other.objects.filter(student = student.user.id)
		for skill in others:
			skills.append(forms.SkillView(skill=skill, category='others'))

		skills.sort(key=lambda instance: instance.value)
		args['skills'] = skills

		return render(request, 'account/profile/edit.html', args)

	else:
	# edit profile (teacher, employer)
		if request.method == 'POST' and 'profile' in request.POST:
			form = forms.EditUser(request.POST, instance = request.user)
			if form.is_valid():
				form.save()
				return redirect('account:profile', username=request.user.username)
		else:
			form = forms.EditUser(instance = request.user)
		args['form'] = form
		
		return render(request, 'account/profile/edit.html', args)




@login_required(login_url="account:login")
def add_skill(request, username = ''):

	#if student profile don't exist create profile
	if models.StudentProfile.objects.filter(user = request.user.id).exists() :
		student = models.StudentProfile.objects.get(user = request.user.id)
	else:
		return redirect('account:add_profile')


	this_url = reverse('account:add_skill', kwargs={'username': request.user.username})
	args = {}

	student = models.Student.objects.get(user = request.user.id)

	if request.method == 'POST' and 'lang' in request.POST:
		lang_form = forms.Lang(request.POST, student=student)
		if lang_form.is_valid():
			lang_form.save()
			return redirect(this_url)
	else:
		lang_form = forms.Lang()
	args['lang_form'] = lang_form	


	if request.method == 'POST' and 'fram' in request.POST:
		fram_form = forms.Fram(request.POST, student=student)
		if fram_form.is_valid():
			fram_form.save()
			return redirect(this_url)
	else:
		fram_form = forms.Fram()
	args['fram_form'] = fram_form


	if request.method == 'POST' and 'other' in request.POST:
		other_form = forms.Other(request.POST, student=student)
		if other_form.is_valid():
			other_form.save()
			return redirect(this_url)
	else:
		other_form = forms.Other()
	args['other_form'] = other_form


	return render(request, 'account/profile/add_skill.html', args)
