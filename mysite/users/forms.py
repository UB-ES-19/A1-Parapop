from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):

	email = forms.EmailField(label = "Email")
	first_name = forms.CharField(label = "Nombre")
	last_name = forms.CharField(label= "Apellido")
	password1 = forms.CharField(label= "Contraseña", widget = forms.PasswordInput)
	password2 = forms.Field(label= "Repetir contraseña", widget = forms.PasswordInput)

	class Meta:

		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']