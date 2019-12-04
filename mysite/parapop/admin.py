from django.contrib import admin
from .models import ProductPost
from .models import Tag


admin.site.register(ProductPost)
admin.site.register(Tag)
