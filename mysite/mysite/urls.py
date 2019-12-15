"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as log_views
from users import views as user_views
from parapop import views as parapop_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', user_views.register, name='register'),
    path('login/', log_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', log_views.LogoutView.as_view(template_name='parapop/index.html'), name='logout'),
    path('', include('parapop.urls')),
    path('profile/', user_views.profile, name='profile'),
    path('products/', parapop_views.products, name='products'),
    url(r'profile/(?P<username>[a-zA-Z0-9]+)$', user_views.get_user_profile),
    path('sell-product/', parapop_views.sell_product, name='sell_product'),
    path('favourites/', parapop_views.favourites, name='favourites'),
    path('update_profile/', user_views.profileUpdate, name='profileUpdate'),
    url(r'^update_product/(?P<productU>.*)/$', parapop_views.updateProduct, name='update_product'),
    path('FAQ/', parapop_views.FAQ, name='FAQ'),
    path('petitions/', user_views.petitions, name='petitions'),
    path('record/', user_views.record, name='record'),
    path('exchange-product/', parapop_views.exchangeProduct, name='exchange_product'),
    url(r'^update_exchange_product/(?P<productU>.*)/$', parapop_views.updateExchangeProduct, name='update_exchange_product')
]

if settings.DEBUG:
    urlpatterns +=staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
