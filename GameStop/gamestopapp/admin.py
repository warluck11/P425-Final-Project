from django.contrib import admin
from gamestopapp.models import Product, Cart, Orders, Review


# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category']
    list_filter = ['category']


admin.site.register(Product, ProductAdmin) 
admin.site.register(Cart)
admin.site.register(Orders)
admin.site.register(Review) 
