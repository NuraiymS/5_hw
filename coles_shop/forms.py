from django import forms
from django.contrib.auth.models import User
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
            ),
        }


class UserRegisterForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={'class': 'Form-control'}
    ))
    password = forms.CharField(max_length=100,
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Password',
                                          'class': 'form-control'}
                               ))
    password1 = forms.CharField(max_length=100,
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Repeat the Password',
                                           'class': 'form-control'}
                                ))

    def clean(self):
        print(self.cleaned_data)
        password = self.cleaned_data['password']
        password1 = self.cleaned_data['password1']
        if password1 != password:
            raise ValidationError('Incorrect password')

        return
