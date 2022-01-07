from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm


# декоратор к функции, чтобы обратиться к ней можно было только методом POST
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd['quantity'],
                 update_quantity=cd['update'])
        # перенаправляем пользователя на адрес cart_detail
        return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    '''Отображает корзину на основе данных в сессии.'''
    cart = Cart(request)
    # создаем объект формы для каждого товара в корзине
    # чтобы пользователь мог сохранить новое кол-во единиц
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                initial={'quantity': item['quantity'],
                                        'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request,
                  'cart/detail.html',
                  {'cart': cart, 'coupon_apply_form': coupon_apply_form})



# Create your views here.
