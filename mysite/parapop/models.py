from django.db import models
from django.contrib.auth.models import User

class ProductPost(models.Model):
	title = models.CharField(max_length = 30)
	description = models.TextField()
	price = models.FloatField()
	date_posted = models.DateTimeField(auto_now_add = True)
	author = models.ForeignKey(User, on_delete= models.CASCADE)
	productPic = models.ImageField(default = 'defaultProduct.jpg', upload_to = 'product_pics')

	def __str__(self):
		return self.title