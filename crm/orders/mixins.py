from django.urls import reverse_lazy

from orders.models import Order


class OrderMixin:
    model = Order
    success_url = reverse_lazy('orders:list')
    template_name = 'orders/order_form.html'
