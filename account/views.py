from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from . import forms
from . import tuples
from . import models

from django.http import HttpResponse


# Create your views here.
def register(request):
	if request.method == 'POST':
		form = forms.Registration(request.POST)
		if form.is_valid():
			form.save()
			return redirect('account:profile')
	else:
		form = forms.Registration()

	args = {'form': form}
	return render(request, 'account/register.html', args)






def reset_password(request):
	return HttpResponse('reset_password')


@login_required(login_url="/account/login/")
def add_skill(request):
	_student = models.Student.objects.get(user = request.user.id)


	if request.method == 'POST':
		form = forms.Add_fram(request.POST)
		if form.is_valid():
			student = form.save(commit=False)
			student.user = request.user
			student.save()

			return redirect('/account/')

	form = forms.Add_fram()

	skill_langs = models.Student_lang.objects.all().filter(student = _student)


	args = {
	'skill_lang': skill_langs,
	'skill_fram': models.Student_fram.objects.all().filter(student = _student),
	'skill_other': models.Student_other.objects.get(student = _student),
	'form': form,
	'student': _student,
	}

	return render(request, 'account/add_skill.html', args)

