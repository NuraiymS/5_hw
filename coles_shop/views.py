import datetime
from unicodedata import category

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import ProductCreateForm, ReviewCreateForm
from .models import Product, Category, Review


# Create your views here.

def hello_world(request):
    return HttpResponse(b'<h1>Hello world</h1>')

def index(request):
    print(request.user.id)
    products = Product.objects.all()
    data= {
        'title': "All products",
        'products': products
    }
    return render(request, 'index.html', context=data)

def product_item(request, id):
    product = Product.objects.get(id=id)

    # reviews = Review.objects.filter(product_id=id)
    # products = Product.objects.filter(id=id)
    data = {
        'product': product,
        # 'reviews': reviews,
        # 'products': products,
    }

    reviews = Review.objects.filter(product_id=id)
    products = Product.objects.filter(id=id)
    data = {
        'product': product,
        'reviews': reviews,
        'products': products,

    }

    return render(request, 'product.html', context=data)

def product_list(request):
    text = request.GET.get('search_text', '')
    products = Product.objects.filter(title__contains=text)
    # print(products)
    # reviews = Review.objects.all()
    try:
        price = int(request.GET.get('price', ''))
        products = products.filter(price=price)
    except:
        pass
    product = request.GET.get('product', '')
    product_selecter = Product.objects.all()
    print(request.GET)
    if product != '':
        print(product)
        products = Product.objects.filter(title=product)


    return render(request,'products.html', context={
        'products': products,
        'product': Product.objects.all(),
        'product_selecter': product_selecter,
    })


def exclude(text):
    pass


def review_list(request):
    text = request.GET.get('search_text', '')
    reviews = Review.objects.all()

    reviews = Review.objects.filter(text__icontains="one", date__gt=datetime.date(2020, 1, 1)).exclude(text='niger')

    return render(request, 'reviews.html', context={
        'reviews': Review.objects.all()

    })

def category_list(request):
    categories = Category.objects.all()
    data = {
        'categories': categories,
    }
    return render(request, 'category.html', context=data)


def review_list(request):
    print(request.user)
    text = request.GET.get('search_text', '')
    reviews = Review.objects.all()

    # reviews = Review.objects.filter(text_contains=text, pub_date_year=2021).exclude(text='niger')
    # reviews = reviews.filter(date=date)
    return render(request, 'reviews.html', context={
        'reviews': reviews
    })


def add_product(request):
    if request.method == 'GET':
        print('GET')
        form = ProductCreateForm()
        data = {
            'form': form
        }
        return render(request, 'add.html', context=data)

    elif request.method == 'POST':
        print('POST')
        print(request.POST)
        form = ProductCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/product/')
        else:
            return render(request, 'add.html',
                          context={'form': form})


@login_required(login_url='/login/')
def add_review(request):
    if request.method == 'GET':
        print('GET')
        form = ReviewCreateForm()
        data = {
            'form': form
        }

        return render(request, 'add_review.html', context=data)

    elif request.method == 'POST':
        print('POST')
        print(request.POST)
        form = ReviewCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('/review/')
        else:
            return render(request,'add_review.html',
                           context={'form': form})

from django.contrib import auth

def login(request):
    # print(request.GET.get('next', ''))
    data = {}
    next = (request.GET.get('next', ''))
    if next:
        data = {
            'message': 'Please authorise to add review'
        }
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            return redirect('/')
        else:
            data['message'] = 'Enter the correct data!'
    return render(request, 'login.html', context=data)


def logout(request):
    auth.logout(request)
    return redirect('/')

