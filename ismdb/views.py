from django.shortcuts import render
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse
# Create your views here.

@login_required(login_url="/account/login/")
def home(request):
	return render(request, "home.html")

def debuging(request):

	langs = '1,2'
	frams = '54,45'
	others = '23,12'
	skill = [langs, frams, others]
	temp = ['1', '45', '0']
	iter = 0
	for i in range(0,3):
		if temp[i] in skill[i]:
			iter += 1
	return HttpResponse(str(iter))

