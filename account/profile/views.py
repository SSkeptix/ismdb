from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from . import forms
from account import tuples
from account import models

from itertools import chain


# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# !!!!!!! need add teacher validation featers

# Show own or someone else's profile
@login_required(login_url="account:login")
def profile(request, username = ''):

	# if url = /account/profile/
	# redirect to show own profile = /account/profile/username/
	user_profile = ( '%s%s/' % (reverse('account:profile'), request.user.username) )
	if (username == '') :
		return redirect(user_profile)

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
		student_profile = models.StudentProfile.objects.get(user = profile.id)

		args['student'] = student_profile
		args['student_lang'] = tuples.LANG().value(student_profile.lang)

	# show skills
		langs = models.Student_lang.objects.filter(student = student_profile.user.id, show=True)
		frams = models.Student_fram.objects.filter(student = student_profile.user.id, show=True)
		others = models.Student_other.objects.filter(student = student_profile.user.id, show=True)

		if langs or frams or others :
			skills = sorted(
				chain(langs, frams, others),
				key=lambda instance: instance.skill.__str__()
				)
		else:
			skills = False

		args['skills'] = skills

	return render(request, 'account/profile/profile.html', args)




@login_required(login_url="account:login")
def add_profile(request):

	user_edit_profile = ( '%s%s/edit/' % (reverse('account:profile'), request.user.username) )
	args = {}

	# add student profile
	if request.method == 'POST' :
		form = forms.AddStudent(request.POST, user=request.user)
		if form.is_valid():
			form.save()
			return redirect(user_edit_profile)
	else:
		form = forms.AddStudent()


	args['form'] = form

	return render(request, 'account/profile/add_profile.html', args)




# Edit own profile
@login_required(login_url="account:login")
def edit_profile(request, username = ''):

	# redirect to edit own profile = /account/profile/username/edit/
	user_edit_profile = ( '%s%s/edit/' % (reverse('account:profile'), request.user.username) )
	if (username == '') or (username != request.user.username) :
		return redirect(user_edit_profile)


	args = {}

	if (request.user.category == tuples.CATEGORY.STUDENT) :

	#if profile don't exist create profile
		if models.StudentProfile.objects.filter(user = request.user.id).exists() :
			student = models.StudentProfile.objects.get(user = request.user.id)
		else:
			return redirect('account:add_profile')

	# edit student profile
		if request.method == 'POST' :
			form = forms.EditUser(request.POST, instance = request.user)
			student_form = forms.EditStudent(request.POST, instance = student)
			if form.is_valid() and student_form.is_valid():
				form.save()
				student_form.save()
				return redirect('%s%s/' % (reverse('account:profile'), request.user.username))
		else:
			form = forms.EditUser(instance = request.user)
			student_form = forms.EditStudent(instance = student)

		args['form'] = form
		args['student_form'] = student_form


	# show skills
		langs = models.Student_lang.objects.filter(student = student.user.id)
		frams = models.Student_fram.objects.filter(student = student.user.id)
		others = models.Student_other.objects.filter(student = student.user.id)

		if langs or frams or others :
			skills = sorted(
				chain(langs, frams, others),
				key=lambda instance: instance.skill.__str__()
				)
		else:
			skills = False

		args['skills'] = skills


		return render(request, 'account/profile/edit.html', args)

	else:
	# edit profile (teacher, employer)
		if request.method == 'POST' :
			form = forms.EditUser(request.POST, instance = request.user)
			if form.is_valid():
				form.save()
				return redirect('%s%s/' % (reverse('account:profile'), request.user.username))
		else:
			form = forms.EditUser(instance = request.user)
		args['form'] = form
		
		return render(request, 'account/profile/edit.html', args)




@login_required(login_url="account:login")
def add_skill(request, username = ''):

	# redirect to edit own profile = /account/profile/username/edit/
	user_add_skill = ( '%s%s/edit/add_skill/' % (reverse('account:profile'), request.user.username) )
	if (username == '') or (username != request.user.username) :
		return redirect(user_add_skill)

	args = {}

	student = models.Student.objects.get(user = request.user.id)

	if request.method == 'POST' and 'lang' in request.POST:
		lang_form = forms.Lang(request.POST, student=student)
		if lang_form.is_valid():
			lang_form.save()
			return redirect(user_add_skill)
	else:
		lang_form = forms.Lang()
	args['lang_form'] = lang_form	


	if request.method == 'POST' and 'fram' in request.POST:
		fram_form = forms.Fram(request.POST, student=student)
		if fram_form.is_valid():
			fram_form.save()
			return redirect(user_add_skill)
	else:
		fram_form = forms.Fram()
	args['fram_form'] = fram_form


	if request.method == 'POST' and 'other' in request.POST:
		other_form = forms.Lang(request.POST, student=student)
		if other_form.is_valid():
			other_form.save()
			return redirect(user_add_skill)
	else:
		other_form = forms.Lang()
	args['other_form'] = other_form


	return render(request, 'account/profile/add_skill.html', args)
