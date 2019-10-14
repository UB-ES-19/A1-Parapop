from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from users import views as user_views
from django.views.generic import CreateView
from .models import ProductPost
from .forms import SellProduct

def home(request):
	queryset = request.GET.get("user_browsed")
	if queryset:
		user = User.objects.filter(username = queryset)
		if (queryset == request.user.username):
			return redirect('../profile')
		else:
			return user_views.get_user_profile(request, queryset)
	else:
		args = {'message_error' : "No error", 'is_error' : False}
		return render(request, 'parapop/index.html', args)

def sell_product(request):
	if request.method == 'POST':
		form = SellProduct(request.POST)
		if form.is_valid():	
			product = form.save(commit = False)
			product.author = request.user
			product.save()
			return redirect('../')
	else:
		form = ProductPost
		args = {'form' : form}
		return render(request, 'parapop/sell_product.html', args)



