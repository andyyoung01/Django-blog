"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views
#from xadmin.plugins import xversion
import xadmin

admin.autodiscover()
#xversion.register_models()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', views.login, name='user_login'),
    url(r'^accounts/logout/$', views.logout, {'next_page': '/'}, name='user_logout'),
    url(r'^search/', include('haystack.urls')),
    url(r'', include('blog.urls')),
    url(r'xadmin/', include(xadmin.site.urls), name='xadmin'),
]

