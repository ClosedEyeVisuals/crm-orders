from django.db.models import F, Sum, Q
from django.views.generic import DetailView, ListView, TemplateView

from orders.models import Order


class HomePage(TemplateView):
    template_name = 'orders/index.html'


class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            ~Q(status='paid')
        ).annotate(
            total_price=Sum(
                F('order_dishes__dish__price') * F('order_dishes__amount')
            )
        ).select_related('table_number').order_by('-created_at')
