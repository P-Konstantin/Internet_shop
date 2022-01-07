from django.db import models
from django.core.validators import MinValueValidator, \
                                    MaxValueValidator


class Coupon(models.Model):
    # код, который используют покупатели
    code = models.CharField(max_length=50, unique=True)
    # дата и время начала действия купона
    valid_from = models.DateTimeField()
    # дата и время окончания действия купона
    valid_to = models.DateTimeField()
    # размер скидки в процентах со значением от 0 до 100
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)])
    # отображения активности купона
    active = models.BooleanField()

    def __str__(self):
        return self.code



# Create your models here.
