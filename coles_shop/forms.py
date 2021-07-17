from django import forms
from django.core.exceptions import ValidationError
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
            'category': Select(
                attrs={
                    'class': 'form-control'
                }
            )

        }

    def clean(self):
        if Product.objects.filter(title=self.cleaned_data['title']):
           raise ValidationError('Takoi product uje est')
        return

class ReviewCreateForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = 'text date product'.split()


        widgets = {
            'date': TextInput
                (
            attrs={
                    'type': 'date',
                }
            )
        }
