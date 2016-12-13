from django.conf.urls import include, url
from blog import views

from blog.models import Post
urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^post/([0-9]+)/$', views.post_detail, name='post-detail'),
]