from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm

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

	
