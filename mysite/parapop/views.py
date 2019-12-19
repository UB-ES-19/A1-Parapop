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
from .forms import ExchangeProduct
from .models import ExchangeProductPost
from users.forms import PetitionForm
from users.models import ExchangePetition
from django.contrib.auth.decorators import login_required
from users.models import Profile
from users.models import Petition
from django.shortcuts import get_object_or_404
from functools import reduce
from operator import or_
from django.core import serializers
from itertools import chain
from datetime import date
import jellyfish
from users import views as users_views
from users.forms import FollowAction
from users.models import Follow

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

	
	if request.POST.get("view_profile"):
		form = FollowAction(request.POST)
		user = User.objects.filter(username=request.POST.get("view_profile"))[0]
		if form.is_valid():
			relation = form.save(commit = False)
			relation.follower = request.user
			relation.following = user
			relation.save()

			followers_count = 0
			followings_count = 0
			followings = Follow.objects.all()
			already_following = False
			for relation in followings:
				if(relation.follower.username == request.user.username and relation.following.username == user.username):
					already_following = True

				if(relation.following.username == user.username):
					followers_count += 1
				elif(relation.follower.username == user.username):
					followings_count += 1

			args = {'followings' : followings, 'user' : user,'already_following' : already_following,'followers_count' : followers_count, 'followings_count' : followings_count, 'logged_in':request.user.is_authenticated}
			return render(request, 'users/user_profile.html', args)
	elif (request.POST.get("profile_user")):
		username = request.POST.get("profile_user")
		return other_user_products(request, username, None,None, False, True, "search")
	elif (request.POST.get("favProduct")):
		text = request.POST.get("favProduct").split(",")
		print(text)
		return other_user_products(request, text[1], text[0], None, False, True,"search")
	elif (request.POST.get("buyProduct")):
		text = request.POST.get("buyProduct").split(",")
		return other_user_products(request, text[1], text[0], None, True, True,"search")
	elif (request.POST.get("exchangeProduct")):
		text = request.POST.get("exchangeProduct").split(",")
		product = ExchangeProductPost.objects.filter(title = text[0])[0]
		yourProducts = ExchangeProductPost.objects.filter(author = request.user)
		return render(request, 'parapop/select_product.html', {'product':product, 'yourProducts': yourProducts})
	elif (request.POST.get("product")):
		text = request.POST.get("product").split(",")
		yourProduct = text[1]
		hisProduct = text[0]
		return other_user_products(request, username, yourProduct, hisProduct, True, False,"search")
	

	petitionForm = PetitionForm()
	queryset = request.GET.get("q",'')
	f_localidad = request.GET.get("loc",'')
	f_precio_maximo = request.GET.get("max_p",'')
	f_data = request.GET.get("date",'')
	petitions = Petition.objects.filter(sender = request.user)
	productPetitions = [petitions[i].product for i in range (len(petitions))]
	l_users = User.objects.none()
	l_products = ProductPost.objects.none()
	l_productsE = ExchangeProductPost.objects.none()

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
				l_products |= ProductPost.objects.filter(title=product.title).exclude(author = request.user)

		productsE = ExchangeProductPost.objects.all()
		for product in productsE:
			if jellyfish.jaro_distance(product.title, queryset) > .60 or jellyfish.jaro_distance(product.description, queryset) > .50:
				l_productsE |= ExchangeProductPost.objects.filter(title=product.title).exclude(author = request.user)
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
		return render(request, 'parapop/search.html', {'fav':True, 'petitions' : productPetitions, 'products' : l_products, 'productsE': l_productsE ,'users':l_users, 'petitionForm':petitionForm})
	else:	
		return render(request, 'parapop/search.html', {'fav':True,'petitions' : productPetitions, 'products' : l_products, 'productsE': l_productsE , 'users':l_users, 'petitionForm':petitionForm})


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
	queryset = ProductPost.objects.filter(author = request.user, purchased_by = None)
	exchange = ExchangeProductPost.objects.filter(author = request.user, purchased_by = None)
	return render(request, 'parapop/products.html', {'user_products' : queryset, 'exchange' : exchange})


def other_user_products(request, username, productName, hisProductName, buyPetition, buyOrExchange, rtype):

	if(productName != None):

		if(buyOrExchange == True):
			if ProductPost.objects.filter(title = productName).count() != 0:
				product = get_object_or_404(ProductPost, title = productName)

				if (buyPetition == True):
					if (request.method == 'POST'):
						reciever = User.objects.filter(username = username)[0]
						product = ProductPost.objects.filter(title = productName)[0]
						form = PetitionForm(request.POST)
						if form.is_valid():
							petition = form.save(commit = False)
							petition.sender = request.user
							petition.reciever = reciever
							petition.product = product
							petition.save()
					elif rtype == "search":
						petition = Petition(sender = User.objects.filter(username = username)[0], reciever = request.user, product = product)
						petition.save()
				else:

					if(product.favUsers.filter(id = request.user.id).exists()):
						product.favUsers.remove(request.user)
					else:
						product.favUsers.add(request.user)

				
			else:
				product = get_object_or_404(ExchangeProductPost, title = productName)
				
				if(product.favUsers.filter(id = request.user.id).exists()):
					product.favUsers.remove(request.user)
				else:
					product.favUsers.add(request.user)
		else:
			print (productName)
			product = get_object_or_404(ExchangeProductPost, title = productName)
			hisProduct = get_object_or_404(ExchangeProductPost, title = hisProductName)
			if (buyPetition == True):
				reciever = User.objects.filter(username = username)[0]
				product = ExchangeProductPost.objects.filter(title = productName)[0]
				hisProduct = ExchangeProductPost.objects.filter(title = hisProductName)[0]
				exchangePetition = ExchangePetition(sender = request.user, reciever = reciever, product = product, hisProduct = hisProduct)
				exchangePetition.save()
			else:
				if(product.favUsers.filter(id = request.user.id).exists()):
					product.favUsers.remove(request.user)
				else:
					product.favUsers.add(request.user)

	profile_user = User.objects.filter(username = username)
	queryset = ProductPost.objects.filter(author = profile_user[0], purchased_by = None)
	exchange = ExchangeProductPost.objects.filter(author = profile_user[0], purchased_by = None)
	disponibleProducts = ExchangeProductPost.objects.filter(author = request.user, purchased_by = None)
	petitions = Petition.objects.filter(sender = request.user)
	productPetitions = [petitions[i].product for i in range (len(petitions))]
	petitionForm = PetitionForm()
	if rtype == "user":
		return render(request, 'parapop/products.html', {'user_products' : queryset,'exchange':exchange, 'fav' : True, 
		'petitionForm':petitionForm, 'petitions': productPetitions, 'disponibleProducts':disponibleProducts})
	else:
		return render(request, 'parapop/index.html')


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



def exchangeProduct(request):
	if request.method == 'POST':
		form = ExchangeProduct(request.POST, request.FILES)
		print(request.POST.getlist('tags'))
		print(Tag.objects.all()[0])
		if form.is_valid():
			product = form.save(commit = False)
			product.author = request.user
			product.save()
			instance = get_object_or_404(ExchangeProductPost, title = request.POST.get("title"))
			for pos in request.POST.getlist('tags'):
				instance.tag.add(Tag.objects.all()[int(pos)-1])
			return redirect('../')
	else:
		form = ExchangeProduct()
		return render(request, 'parapop/exchange_product.html', {'form' : form})

def updateExchangeProduct(request,productU):
	if request.method == 'POST':
		instance = ExchangeProductPost.objects.filter(title = productU)
		productForm = ExchangeProduct(request.POST, request.FILES, instance = instance[0])
		if productForm.is_valid():
			productForm.save()
			instance[0].tag.clear()
			for pos in request.POST.getlist('tags'):
				instance[0].tag.add(Tag.objects.all()[int(pos)-1])
			return products(request)
	else:
		instance = ExchangeProductPost.objects.filter(title = productU)
		productForm = ExchangeProduct(instance = instance[0])
		tagList = []
		for tag in instance[0].tag.all():
			tagList.append(tag)

		args = {'productForm' : productForm, 'tagList' : tagList}

	return render(request, 'parapop/update_exchange_product.html', args)
