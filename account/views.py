from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import update_session_auth_hash
from . import forms
from . import tuples
from . import models

from django.http import HttpResponse



def register(request):
	if request.method == 'POST':
		form = forms.Registration(request.POST)
		if form.is_valid():
			form.save()
			return redirect('account:login')
	else:
		form = forms.Registration()

	args = {
		'form': form,
	}
	return render(request, 'account/register.html', args)



def change_password(request):
	if request.method == 'POST':
		form = forms.ChangePassword(data=request.POST, user=request.user)

		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			return redirect('account:profile', username=request.user.username)
	else:
		form = forms.ChangePassword(user=request.user)

	args = {'form': form, }
	return render(request, 'account/change_password.html', args)


