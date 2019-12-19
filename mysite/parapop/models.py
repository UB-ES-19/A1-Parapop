from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):	
	description = models.CharField(max_length=300)
	def __str__(self):
		return self.description
class ProductPost(models.Model):
	title = models.CharField(max_length = 30)
	description = models.TextField()
	price = models.FloatField()
	author = models.ForeignKey(User, on_delete= models.CASCADE, blank = True)
	productPic = models.FileField(upload_to = 'product_pics/')
	favUsers = models.ManyToManyField(User, related_name = 'favUsers', blank = True)
	pub_date = models.DateField(auto_now_add=True, null=True, blank=True)
	tag = models.ManyToManyField(Tag) 
	purchased_by = models.ForeignKey(User, related_name = 'purchased_by', on_delete= models.CASCADE, blank = True, null = True)
	score = models.IntegerField(blank = True, null = True)

	def __str__(self):
		return self.title

class ExchangeProductPost(models.Model):
	title = models.CharField(max_length = 30)
	description = models.TextField()
	author = models.ForeignKey(User, on_delete= models.CASCADE, blank = True)
	productPic = models.FileField(upload_to = 'product_pics/')
	favUsers = models.ManyToManyField(User, related_name = 'EfavUsers', blank = True)
	tag = models.ManyToManyField(Tag) 
	purchased_by = models.ForeignKey(User, related_name = 'Epurchased_by', on_delete= models.CASCADE, blank = True, null = True)
	score = models.IntegerField(blank = True, null = True)

	def __str__(self):
		return self.title



