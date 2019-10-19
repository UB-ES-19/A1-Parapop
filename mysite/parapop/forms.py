from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ProductPost

class SellProduct(forms.ModelForm):

	class Meta:
		model = ProductPost
		fields = ('title', 'description', 'price','productPic',)
