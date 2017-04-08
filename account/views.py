from django.shortcuts import render, redirect
from . import forms
from .tuples import GROUP
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse


# Create your views here.
def register(request):
	if request.method == 'POST':
		form = forms.RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			next_page = '/'
			if form.cleaned_data['group'] == GROUP.STUDENT:
				next_page = '/account/add_skills/'
			else:
				next_page = '/'

			return redirect(next_page)
			#return HttpResponse(next_page)
	else:
		form = forms.RegistrationForm()

	args = {'form': form}
	return render(request, 'account/register.html', args)



def reset_password(request):
	return HttpResponse('reset_password')

@login_required(login_url="/account/login/")
def account(request):
	return HttpResponse('account')

@login_required(login_url="/account/login/")
def add_skill(request):
	#form = Add_skill()
	args = {'form': form}
	return render(request, 'account/add_skill.html', args)