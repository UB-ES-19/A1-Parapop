from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from .forms import FollowAction
from django.contrib.auth.decorators import login_required
from .models import Follow
from .models import Profile
from django.contrib.auth.models import User

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			return redirect('homepage')

	else:
		form = UserRegisterForm()
	return render(request,'users/register.html',{'form': form})

@login_required
def products(request):

	return render(request, 'users/products.html')

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
	try:
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
	except Exception:
		args = {'message_error' : "Usuario no encontrado!", 'is_error' : True}

		return render(request, 'parapop/index.html', args)
