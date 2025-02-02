from django.urls import reverse_lazy

from orders.models import Order


class OrderEditMixin:
    model = Order
    pk_url_kwarg = 'order_id'
    success_url = reverse_lazy('orders:list')
