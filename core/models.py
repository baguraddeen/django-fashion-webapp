from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse



class Category(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name 


class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    thumbnail_1  = models.ImageField(upload_to='items_pics/')
    thumbnail_2  = models.ImageField(upload_to='items_pics/' )
    thumbnail_3  = models.ImageField(upload_to='items_pics/')
    total_views = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField('Category', related_name='posts')
    featured = models.BooleanField()
    show_to_friends = models.BooleanField()


    def __str__(self):
        return self.title

    
    def get_absolute_url(self):
        return reverse('core:product_detail', args=[self.id])