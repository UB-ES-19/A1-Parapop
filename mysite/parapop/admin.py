from django.contrib import admin
from .models import ProductPost
from .models import Tag
from .models import ExchangeProductPost


admin.site.register(ProductPost)
admin.site.register(Tag)
admin.site.register(ExchangeProductPost)

