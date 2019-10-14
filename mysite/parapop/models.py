from django.db import models
from django.contrib.auth.models import User

class ProductPost(models.Model):
	title = models.CharField(max_length = 30)
	description = models.TextField()
	price = models.FloatField()
	author = models.ForeignKey(User, on_delete= models.CASCADE, blank = True)
	productPic = models.ImageField(default = 'defaultProduct.jpg', upload_to = 'product_pics')

	def __str__(self):
		return self.title