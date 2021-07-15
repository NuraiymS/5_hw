from django.contrib import admin

# Register your models here.
from coles_shop.models import Product, Category, Review


class ProductInline(admin.StackedInline):
    model = Product
    fields = 'title'.split()
    extra = 2


class CategoryAdmin(admin.ModelAdmin):
    inlines = [ProductInline]


class ProductAdmin(admin.ModelAdmin):
    list_display = 'id title price category'.split()
    search_fields = 'title'.split()
    list_filter = 'price category'.split()
    list_editable = 'title category'.split()


class ReviewInline(admin.StackedInline):
    model = Review
    fields = 'text'.split()
    extra = 2


class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


class ReviewAdmin(admin.ModelAdmin):
    list_display = 'id product text'.split()


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
