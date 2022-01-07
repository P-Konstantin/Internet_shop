from django.shortcuts import render, get_object_or_404, redirect
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


def order_create(request):
    # получаем объект корзины
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                # проходим по всем товарам коризины и создаем
                # для каждого объект OrderItem
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            # запуск асинхронной задачи
            order_created.delay(order.id)
            # сохранение заказа в сессии
            request.session['order_id'] = order.id
            # перенаправление на страницу оплаты
            return redirect(reverse('payment:process'))

    else:
        # при получении запроса GET инициируем форму и передаем её в шаблон
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                      {'cart': cart, 'form': form})


# декоратор проверяет, что у пользователя в полях
# is_active и is_staff сохранено значение True
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
                  'admin/orders/order/detail.html',
                  {'order': order})


# декоратор, чтобы доступ к функции имели только администраторы
@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content_Disposition'] = 'filename=\
        "order_{}.pdf"'.format(order.id)
    weasyprint.HTML(string=html).write_pdf(response,
                            stylesheets=[weasyprint.CSS(
                                settings.STATIC_ROOT + 'css/pdf.css')])
    return response




