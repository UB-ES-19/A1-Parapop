from django.contrib import admin
from .models import Profile
from .models import Follow
from .models import Location
from .models import Petition
from .models import ExchangePetition

admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Location)
admin.site.register(Petition)
admin.site.register(ExchangePetition)