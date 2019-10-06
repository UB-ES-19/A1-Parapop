from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from .models import Follow
from .models import Profile

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
	profileUser = Profile.user
	user = request.user
	args = {'followings' : followings, 'profileUser': profileUser, 'user':user}
	return render(request, 'users/profile.html', args)

@login_required
def follow(request):
	if(request.method == 'POST'):
		form = FollowForm(request.POST)
		if form.is_valid:
			form.save()
	return render(request, 'users/profile.html', args)


