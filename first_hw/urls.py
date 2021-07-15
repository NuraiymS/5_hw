"""first_hw URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from coles_shop import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hello', views.hello_world),
    path('', views.index),
    path('products/<int:id>/', views.product_item),
    path('product/', views.product_list),
    path('review/', views.review_list),
    path('category', views.category_list),
    path('add_product/',views.add_product),
    path('add_review/', views.add_review),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

