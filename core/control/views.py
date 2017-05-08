from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from account import models
from account import tuples
from django.http import Http404, HttpResponse

from core.functions import validation_permission




def user_validation(request):
	args = {'validation_permission': validation_permission(user = request.user), }

	if not args['validation_permission']:
		return redirect('404')
		
	users = models.User.objects.filter(validated_by__isnull = True).only('first_name', 'last_name', 'username', 'date_joined').order_by('last_name', 'first_name')
	args['users'] = users 

	return render(request, 'core/control/user_validation.html', args)





