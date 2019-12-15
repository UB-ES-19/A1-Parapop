from django.db import models
from django.contrib.auth.models import User	
from parapop.models import ProductPost
from parapop.models import ExchangeProductPost

class Location(models.Model):	
	location = models.CharField(max_length=30)
	def __str__(self):
		return self.location

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True)
	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
	location = models.ManyToManyField(Location)
	def __str__(self):
		return f'{self.user.username} profile'

class Follow(models.Model):
	follower = models.ForeignKey(User, related_name="who_is_followed", on_delete = models.CASCADE, blank = True)
	following = models.ForeignKey(User, related_name="who_follows", on_delete = models.CASCADE, blank = True)
      

	def __str__(self):
		return f'{self.follower.username}'

class Petition(models.Model):
	sender = models.ForeignKey(User, related_name="sender", on_delete = models.CASCADE, blank = True)
	reciever = models.ForeignKey(User, related_name="reciever", on_delete = models.CASCADE, blank = True)
	product = models.ForeignKey(ProductPost, related_name="product", on_delete = models.CASCADE, blank = True)
	currentState = models.CharField(max_length=15, default = "Pending")
	def __str__(self):
		return f'From {self.sender.username} to {self.reciever.username}'

class ExchangePetition(models.Model):
	sender = models.ForeignKey(User, related_name="Esender", on_delete = models.CASCADE, blank = True)
	reciever = models.ForeignKey(User, related_name="Ereciever", on_delete = models.CASCADE, blank = True)
	product = models.ForeignKey(ExchangeProductPost, related_name="Eproduct", on_delete = models.CASCADE, blank = True)
	hisProduct = models.ForeignKey(ExchangeProductPost, related_name="EhisProduct", on_delete = models.CASCADE, blank = True)
	currentState = models.CharField(max_length=15, default = "Pending")
	def __str__(self):
		return f'From {self.sender.username} to {self.reciever.username}'



