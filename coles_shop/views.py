import datetime
import json
import secrets
from unicodedata import category

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from .forms import ProductCreateForm, ReviewCreateForm, UserRegisterForm
from .models import Product, Category, Review, ConfirmCode


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

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=request.POST['email'],

                is_active=False
            )
            user.set_password(raw_password=request.POST['password'])
            code = secrets.token_urlsafe(16)
            ConfirmCode.objects.create(user=user, code=code)
            send_mail(
                subject='Activation Code',
                message=f'http://127.0.0.1:8000/activate/{code}/',
                from_email=settings.EMAIL_HOST,
                recipient_list=[request.POST['email']]
            )
        else:
            return render(request, 'register.html', context={
                'form': form
            })
    data = {
        'form': UserRegisterForm()
    }
    print(data)
    return render(request, 'register.html', context=data)

def activate_code(request, code):
    user=ConfirmCode.objects.filter(code=code).first()
    if user:
        user=user.user
    auth.login(request=request, user=user)
    products=Product.objects.all()

    return render(request, 'layout.html', context={'products': products})


def product_count(request):
    count = Product.objects.all().count()
    return JsonResponse(data={'count': count})

@csrf_exempt
def search(request):
    if request.method == 'POST':
        text = json.loads(request.body).get('search_text', '')
        products = Product.objects.filter(name__contains=text)
        return JsonResponse(data=list(products.values()), safe=False)


def product_search(request):
    return render(request, 'search.html')