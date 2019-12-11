from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from .forms import FollowAction
from .forms import ProfileCreation, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from .models import Follow
from .models import Profile
from .models import Location
from .models import Petition
from parapop.models import ProductPost
from django.contrib.auth.models import User
from parapop import views as parapop_views
from django.shortcuts import get_object_or_404

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()		
			username = form.cleaned_data.get('username')
			user = User.objects.filter(username = username)
			locationPos = request.POST.getlist('localización')[0]
			location = Location.objects.all()[int(locationPos)-1]
			try:
				im = request.FILES["image"]	
				Profile.objects.create(user = user[0], image = im)
			except:
				Profile.objects.create(user = user[0])

			instance = get_object_or_404(Profile, user = user[0])
			print(location)
			instance.location.add(location)

			return redirect('homepage')
		else:
			form = UserRegisterForm()
			profileForm = ProfileCreation()
			return render(request,'users/register.html',{'form': form, 'profileForm': profileForm})
	else:
		form = UserRegisterForm()
		profileForm = ProfileCreation()
		return render(request,'users/register.html',{'form': form, 'profileForm': profileForm})


def login(request):
	return render(request,'users/login.html')


def logout(request):
	logout(request)
	return redirect('http://localhost:8000')

@login_required
def profile(request):
	followings = Follow.objects.all()

	followers_count = 0
	followings_count = 0

	for relation in followings:
		if(relation.following.username == request.user.username):
			followers_count += 1
		elif(relation.follower.username == request.user.username):
			followings_count += 1

	args = {'followers_count' : followers_count, 'followings_count' : followings_count}

	return render(request, 'users/profile.html', args)

def get_user_profile(request, username):
	
	user = User.objects.get(username=username)

	if (user == request.user):
		return redirect('../profile')

	elif request.method == 'POST':
		form = FollowAction(request.POST)
		if request.POST.get("follow"):
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
			return parapop_views.other_user_products(request, username, None, False)
		elif (request.POST.get("favProduct")):
			productName = request.POST.get("favProduct")
			return parapop_views.other_user_products(request, username, productName, False)
		elif (request.POST.get("buyProduct")):
			productName = request.POST.get("buyProduct")
			return parapop_views.other_user_products(request, username, productName, True)
		else:
			if form.is_valid():

				Follow.objects.filter(follower = request.user, following = user).delete()

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
	
	else:
		followings = Follow.objects.all()
		form = FollowAction
		form.following = user
		form.follower = request.user

		followers_count = 0
		followings_count = 0
		already_following = False
		for relation in followings:
			if(relation.follower.username == request.user.username and relation.following.username == user.username):
				already_following = True

			if(relation.following.username == user.username):
				followers_count += 1
			elif(relation.follower.username == user.username):
						followings_count += 1

		args = {'followings' : followings, 'user' : user,'form' : form, 'already_following' : already_following, 'followers_count' : followers_count,'followings_count' : followings_count, 'logged_in':request.user.is_authenticated}
		return render(request, 'users/user_profile.html', args)

	args = {'message_error' : "Usuario no encontrado!", 'is_error' : True}

	return render(request, 'parapop/index.html', args)

@login_required
def profileUpdate(request):
	if request.method == 'POST':
		userForm = UserUpdateForm(request.POST, instance = request.user)
		profileForm = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
		if (userForm.is_valid() and profileForm.is_valid()):
			userForm.save()
			profileForm.save()
			return profile(request)

	else:
		userForm = UserUpdateForm(instance = request.user)
		profileForm = ProfileUpdateForm(instance = request.user.profile)
		args = {'userForm': userForm, 'profileForm' : profileForm}

	return render(request, 'users/profile_update.html', args)

@login_required
def petitions(request):
	if request.POST.get("accept"):
		product = ProductPost.objects.filter(title = request.POST.get("accept"))[0]
		print(product)
		petition = Petition.objects.filter(reciever = request.user, product = product)
		petition.update(currentState = "Accepted")
		ProductPost.objects.filter(title = request.POST.get("accept")).update(purchased_by = petition[0].sender)
	elif request.POST.get("deny"):
		product = ProductPost.object.filter(title = request.POST.get("accept"))
		petition = Petition.object.get(reciever = request.user, product = product)
		petition.update(currentState = "Denied")

	pendingRecievedPetitions = Petition.objects.filter(reciever = request.user, currentState = "Pending")
	print(pendingRecievedPetitions)
	pendingSentPetitions = Petition.objects.filter(sender = request.user, currentState = "Pending")
	acceptedRecievedPetitions = Petition.objects.filter(reciever = request.user, currentState = "Accepted")
	acceptedSentPetitions = Petition.objects.filter(sender = request.user, currentState = "Accepted")
	deniedRecievedPetitions = Petition.objects.filter(reciever = request.user, currentState = "Denied")
	deniedSentPetitions = Petition.objects.filter(sender = request.user, currentState = "Denied")
	args = {'pendingRecievedPetitions': pendingRecievedPetitions, 'pendingSentPetitions':pendingSentPetitions,
	'acceptedRecievedPetitions':acceptedRecievedPetitions, 'acceptedSentPetitions':acceptedSentPetitions,
	'deniedRecievedPetitions': deniedRecievedPetitions, 'deniedSentPetitions': deniedSentPetitions}
	return render(request, 'users/petitions.html', args)

@login_required
def record(request):
	soldProducts = ProductPost.objects.filter(author = request.user).exclude(purchased_by = None)
	purchasedProducts = ProductPost.objects.filter(purchased_by = request.user)
	args = {'soldProducts' : soldProducts, 'purchasedProducts' : purchasedProducts}
	return render(request, 'users/record.html', args)

