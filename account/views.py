from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
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

	args = {'form': form}
	return render(request, 'account/register.html', args)


def reset_password(request):
	return HttpResponse('reset_password')

