from django.db.models import F, Sum, Q
from django.urls import reverse_lazy
from django.views.generic import (DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)


from orders.forms import OrderForm
from orders.mixins import OrderEditMixin
from orders.models import Order


class HomePage(TemplateView):
    template_name = 'orders/index.html'


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(
            total_price=Sum(
                F('order_dishes__dish__price') * F('order_dishes__amount')
            )
        ).select_related('table_number').order_by('-created_at')


class OrderUpdateView(OrderEditMixin, UpdateView):
    form_class = OrderForm


class OrderDeleteView(OrderEditMixin, DeleteView):
    template_name = 'orders/order_form.html'
