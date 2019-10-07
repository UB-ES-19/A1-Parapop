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

def login(request):
	return render(request,'users/login.html')


def logout(request):
	logout(request)
	return render(request, 'homepage')

@login_required
def profile(request):
	followings = Follow.objects.all()
	args = {'followings' : followings}

	return render(request, 'users/profile.html', args)

@login_required
def get_user_profile(request, username):

	user = User.objects.get(username=username)
	if (user == request.user):
		return redirect('../profile')
	elif request.method == 'POST':
		form = FollowAction(request.POST)
		if form.is_valid():
			print("A")
			relation = form.save(commit = False)
			relation.follower = request.user
			relation.following = user
			relation.save()
			followings = Follow.objects.all()
			args = {'followings' : followings, 'user' : user}
			return render(request, 'users/user_profile.html', args)
	else:
		followings = Follow.objects.all()
		args = {'followings' : followings, 'user' : user}
		form = FollowAction
		form.following = user
		form.follower = request.user 
		args = {'followings' : followings, 'user' : user,'form' : form}
		return render(request, 'users/user_profile.html', args)


