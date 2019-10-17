from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Follow
from .models import Profile


class UserRegisterForm(UserCreationForm):

	email = forms.EmailField(label = "Email", required=True)
	first_name = forms.CharField(label = "Nombre")
	last_name = forms.CharField(label= "Apellido")
	password1 = forms.CharField(label= "Contraseña", widget = forms.PasswordInput)
	password2 = forms.Field(label= "Repetir contraseña", widget = forms.PasswordInput)

	class Meta:

		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

	def clean_email(self):
		data = self.cleaned_data['email']
		if User.objects.filter(email=data).exists():
			raise forms.ValidationError("This email already used")
		return data

class FollowAction(forms.ModelForm):

	class Meta:
		model = Follow
		fields = ['follower', 'following']
		widgets = {'follower': forms.HiddenInput(),'following': forms.HiddenInput() }

class ProfileCreation(forms.ModelForm):

	class Meta:
		model = Profile
		fields = ['user', 'image']
