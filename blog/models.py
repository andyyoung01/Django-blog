from __future__ import unicode_literals

# Create your models here.
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Tag(models.Model):
    class Meta:
        app_label = 'blog'
        verbose_name = 'tag'
        verbose_name_plural = 'tag'

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Category(models.Model):
    class Meta:
        app_label = 'blog'
        verbose_name = 'category'
        verbose_name_plural = 'category'

    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Post(models.Model):
    class Meta:
        verbose_name = u'article'
        verbose_name_plural = u'article'
    author = models.ForeignKey(User)
    title = models.CharField(max_length=200)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    category = models.ForeignKey(Category)
    click = models.IntegerField(default=0)
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
