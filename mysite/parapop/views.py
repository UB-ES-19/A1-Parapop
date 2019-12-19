from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.db.models import Q
from users import views as user_views
from django.views.generic import CreateView
from .models import ProductPost
from .models import Tag
from .forms import SellProduct
from django.contrib.auth.decorators import login_required
from users.models import Profile
from django.shortcuts import get_object_or_404
from functools import reduce
from operator import or_
from django.core import serializers
from itertools import chain
from datetime import date
import jellyfish

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

def busqueda(request):

	queryset = request.GET.get("q",'')
	f_localidad = request.GET.get("loc",'')
	f_precio_maximo = request.GET.get("max_p",'')
	f_data = request.GET.get("date",'')

	l_users = User.objects.none()
	l_products = ProductPost.objects.none()

	filtered = False
	if queryset != "":
		# -- Buscamos los usuarios en la base.
		users = User.objects.all()
		for user in users:
			if jellyfish.jaro_distance(user.username, queryset) > .65:
				l_users |= User.objects.filter(username=user.username) 
		
		# -- Buscamos los productos en la base y luego los filtramos.
		products = ProductPost.objects.all()
		for product in products:
			if jellyfish.jaro_distance(product.title, queryset) > .60 or jellyfish.jaro_distance(product.description, queryset) > .50:
				l_products |= ProductPost.objects.filter(title=product.title)

		# -- Filtramos por localidad.
		if f_localidad != "":
			filtered = True
			f_localidad_products = ProductPost.objects.none()
			for product in l_products:
				if jellyfish.jaro_distance(str(product.author.profile.location.first()), f_localidad) > .75:			
					f_localidad_products |= ProductPost.objects.filter(title=product.title)
			l_products &= f_localidad_products
		
		# -- Filtramos por precio.
		if f_precio_maximo != "":
			filtered = True
			f_precio_products = ProductPost.objects.none()
			for product in l_products:
				if product.price <= float(f_precio_maximo):			
					f_precio_products |= ProductPost.objects.filter(title=product.title)
			l_products &= f_precio_products

		# -- Filtramos por la data seleccionada.
		if f_data != "":
			filtered = True
			f_data_products = ProductPost.objects.none()
			for product in l_products:
				if str(product.pub_date) >= f_data:			
					f_data_products |= ProductPost.objects.filter(title=product.title)
			l_products &= f_data_products


	if filtered:
		return render(request, 'parapop/search.html', {'products' : l_products, 'users':l_users})
	else:	
		return render(request, 'parapop/search.html', {'products' : l_products, 'users':l_users})


def sell_product(request):
	if request.method == 'POST':
		form = SellProduct(request.POST, request.FILES)
		print(request.POST.getlist('tags'))
		print(Tag.objects.all()[0])
		if form.is_valid():
			product = form.save(commit = False)
			product.author = request.user
			product.save()
			instance = get_object_or_404(ProductPost, title = request.POST.get("title"))
			for pos in request.POST.getlist('tags'):
				instance.tag.add(Tag.objects.all()[int(pos)-1])
			return redirect('../')
	else:
		form = SellProduct()
		return render(request, 'parapop/sell_product.html', {'form' : form})


def products(request):
	queryset = ProductPost.objects.filter(author = request.user)
	print(queryset)
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

def updateProduct(request,productU):
	if request.method == 'POST':
		instance = ProductPost.objects.filter(title = productU)
		productForm = SellProduct(request.POST, request.FILES, instance = instance[0])
		if productForm.is_valid():
			productForm.save()
			instance[0].tag.clear()
			for pos in request.POST.getlist('tags'):
				instance[0].tag.add(Tag.objects.all()[int(pos)-1])
			return products(request)
	else:

		instance = ProductPost.objects.filter(title = productU)
		productForm = SellProduct(instance = instance[0])
		tagList = []
		for tag in instance[0].tag.all():
			tagList.append(tag)

		args = {'productForm' : productForm, 'tagList' : tagList}

	return render(request, 'parapop/update_product.html', args)

def FAQ(request):
	return render(request, 'parapop/FAQ.html')
