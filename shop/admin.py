from django.contrib import admin
from .models import Category, Product


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    # настраиваем поле slug, оно формирется из поля name
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    # поля должны быть добавлены в list_display для их отображения
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    # поле для фильтрации объектов
    list_filter = ['available', 'created', 'updated']
    # можно изменять поля со страницы списка товаров, не переходя к форме их редактирования
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Product, ProductAdmin)



# Register your models here.
