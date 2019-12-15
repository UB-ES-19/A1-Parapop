from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import ProductPost
from .models import ExchangeProductPost
from .models import Tag

TAGS = ['Vehículo', 'Moda y accesorios', 'Inmobiliaria', 'TV, Audio y Foto', 'Informática y Electrónica', 
		'Deporte y Ocio', 'Consolas y Videojuegos', 'Hogar y Jardín', 'Electrodomésticos', 'Cine, Libros y Música',
		'Niños y Bebés', 'Coleccionismo', 'Materiales de construcción', 'Industria y Agricultura', 'Empleo', 'Servicios']

class SellProduct(forms.ModelForm):
	tags =  forms.ModelMultipleChoiceField(queryset = Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
	class Meta:
		model = ProductPost
		fields = ('title', 'description', 'price','productPic')

class ExchangeProduct(forms.ModelForm):
	tags =  forms.ModelMultipleChoiceField(queryset = Tag.objects.all(), required=False, widget=forms.CheckboxSelectMultiple)
	class Meta:
		model = ExchangeProductPost
		fields = ('title', 'description','productPic')

