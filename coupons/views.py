from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    # используем timezone.now(), чтобы получить объект даты и времени
    # с учетом временно зоны
    now = timezone.now()
    # создаем форму на основе переданных данных
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        # получаем код из словаря
        code = form.cleaned_data['code']
        try:
            # используем iexact, чтобы проверить код без учёта регистра
            # купон должен быть активным active=True
            # сравниваем время с временем начала окончания:
            # lte - меньше или равно, gte - больше или равно
            coupon = Coupon.objects.get(code__iexact=code,
                                        valid_from__lte=now,
                                        valid_to__gte=now,
                                        active=True)
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:cart_detail')

# Create your views here.
