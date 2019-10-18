from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from users import views as user_views
from django.views.generic import CreateView
from .models import ProductPost
from .forms import SellProduct
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.shortcuts import get_object_or_404

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
		form = SellProduct(request.POST, request.FILES)
		if form.is_valid():	
			product = form.save(commit = False)
			product.author = request.user
			product.save()
			return redirect('../')
	else:
		form = SellProduct()
		return render(request, 'parapop/sell_product.html', {'form' : form})


def products(request):
	queryset = ProductPost.objects.filter(author = request.user)
	return render(request, 'parapop/products.html', {'user_products' : queryset})

def other_user_products(request, username, productName):
	if(productName != None):
		product = get_object_or_404(ProductPost, title = productName)
		if(product.favUsers.filter(id = request.user.id).exists()):
			product.favUsers.remove(request.user)
		else:
			product.favUsers.add(request.user)
	profile_user = User.objects.filter(username = username)
	queryset = ProductPost.objects.filter(author = profile_user[0])
	return render(request, 'parapop/products.html', {'user_products' : queryset, 'fav' : True})

def favourites(request):
	queryset = ProductPost.objects.filter(favUsers__id = request.user.id)
	return render(request, 'parapop/favourites.html', {'user_products' : queryset})