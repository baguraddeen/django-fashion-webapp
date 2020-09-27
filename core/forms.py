from django import forms
from .models import Product




class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'thumbnail_1', 'thumbnail_2', 'thumbnail_3', 'categories', 'featured', 'show_to_friends')