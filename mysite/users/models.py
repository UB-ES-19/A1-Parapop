from django.db import models
from django.contrib.auth.models import User	


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE, blank = True)
	image = models.ImageField(default = 'default.jpg', upload_to = 'profile_pics')
	def __str__(self):
		return f'{self.user.username} profile'

class Follow(models.Model):
	follower = models.ForeignKey(User, related_name="who_is_followed", on_delete = models.CASCADE, blank = True)
	following = models.ForeignKey(User, related_name="who_follows", on_delete = models.CASCADE, blank = True)
      

	def __str__(self):
		return f'{self.follower.username}'





