from django.contrib import admin
from .models import Profile
from .models import Follow
from .models import Location

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Location)