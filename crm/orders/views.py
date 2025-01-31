from django.views.generic import ListView

from orders.models import Order


class HomePage(ListView):
    queryset = Order.objects.all()
    template_name = 'orders/index.html'
