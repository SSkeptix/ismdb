from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from . import forms
from account import tuples
from account import models

from django.http import HttpResponse



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


	user = request.user
	profile = models.User.objects.get(username = username)
	if (user.category == tuples.CATEGORY.TEACHER) :
		is_teacher = True
	else:
		is_teacher = False
	args = {
		'is_teacher': is_teacher,
	}

	# if user want to view profile of student
	if (profile.category == tuples.CATEGORY.STUDENT) :
		student = models.Student.objects.get(user = profile.id)

		args['student'] = student
		args['student_lang'] = tuples.LANG().value(student.lang)
		args['langs'] = models.Student_lang.objects.filter(student = student)
		args['frams'] = models.Student_fram.objects.filter(student = student)
		args['others'] = models.Student_other.objects.filter(student = student)

		return render(request, 'account/profile/student_profile.html', args)
	

	# if user want to view profile of teacher or employer
	else:
		args['user'] = profile
		return render(request, 'account/profile/profile.html', args)




# Edit own profile
@login_required(login_url="account:login")
def edit_profile(request, username = ''):

	# redirect to edit own profile = /account/profile/username/edit/
	user_edit_profile = ( '%s%s/edit/' % (reverse('account:profile'), request.user.username) )
	if (username == '') or (username != request.user.username) :
		return redirect(user_edit_profile)


	args = {}


	if (request.user.category == tuples.CATEGORY.STUDENT) :

		if request.method == 'POST':
			form = forms.EditUser(request.POST, instance = request.user)
			if form.is_valid():
				form.save()
				return redirect('%s%s/' % (reverse('account:profile'), request.user.username))

		else:
			form = forms.EditUser(instance = request.user)

		args['form'] = form
		
		return render(request, 'account/profile/edit_student.html', args)


	else:

		if request.method == 'POST':
			form = forms.EditUser(request.POST, instance = request.user)
			if form.is_valid():
				form.save()
				return redirect('%s%s/' % (reverse('account:profile'), request.user.username))

		else:
			form = forms.EditUser(instance = request.user)

		args['form'] = form
		
		return render(request, 'account/profile/edit_user.html', args)








	return HttpResponse('edit_profile')
