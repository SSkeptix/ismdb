from django.shortcuts import render, redirect
from .forms import RegistrationForm as UserCreationForm
from .users import GROUP
from django.contrib.auth.decorators import login_required

from django.http import HttpResponse


# Create your views here.
def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
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
		form = UserCreationForm()

	args = {'form': form}
	return render(request, 'account/register.html', args)



def reset_password(request):
	return HttpResponse('reset_password')

@login_required(login_url="/account/login/")
def account(request):
	return HttpResponse('account')

@login_required(login_url="/account/login/")
def add_skills(request):
	return HttpResponse('add_skills')