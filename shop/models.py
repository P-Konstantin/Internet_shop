from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)


    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                       args=[self.slug])

class Product(models.Model):
    # каждый товар - одна категория, категия - множесто товаров
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    # поле слага для создания понятных urls
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m?/%d', blank=True)
    description = models.TextField(blank=True)
    # цена, max_digits - макс. число цифр, decimal_places - число цифр после запятой
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    # наличие товара
    available = models.BooleanField(default=True)
    # дата и время создания товара
    created = models.DateTimeField(auto_now_add=True)
    # дата и время последнего изменения товара
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ('name',)
        # запрашиваем товары по id и slug для ускорения выборки объектов
        index_together = (('id', 'slug'),)


    def __str__(self):
        return self.name


    def get_absolute_url(self):
        return reverse('shop:product_detail',
                       args=[self.id, self.slug])


