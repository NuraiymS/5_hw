from django import forms
from django.forms import TextInput, NumberInput, Select

from .models import Product, Review


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = 'title description price category'.split()
        widgets = {
            'title': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the name of product'
                }
            ),
            'description': TextInput(
                attrs={
                    'class': 'form-control',
                }
            ),
            'price': NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),
            'course': Select(
                attrs={
                    'class': 'form-control'
                }
            )

        }



class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = 'text data product'.split()

