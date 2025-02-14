from django.db import transaction
from django.db.models import F, Sum
from django.views.generic import (CreateView, DeleteView, DetailView,
                                  TemplateView, UpdateView)

from django_filters.views import FilterView


from orders.filters import OrderDateRangeFilter, OrderFilter
from orders.forms import DishFormSet, OrderForm
from orders.mixins import OrderMixin
from orders.models import Category, Order


class HomePage(TemplateView):
    template_name = 'orders/index.html'


class OrderListView(FilterView):
    model = Order
    template_name = 'orders/order_list.html'
    filterset_class = OrderFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(
            total_price=Sum(
                F('order_dishes__dish__price') * F('order_dishes__amount')
            )
        ).select_related('table_number').order_by('-created_at')


class OrderPaidListView(OrderListView):
    filterset_class = OrderDateRangeFilter

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(status='paid')

    @staticmethod
    def get_total(queryset):
        return queryset.aggregate(Sum('total_price'))

    def get_context_data(self, **kwagrs):
        context = super(OrderPaidListView, self).get_context_data(**kwagrs)
        object_list = context['object_list']
        context['total'] = self.get_total(object_list)
        return context


class OrderCreateView(OrderMixin, CreateView):
    form_class = OrderForm

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['dish_formset'] = DishFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        dish_formset = context['dish_formset']
        with transaction.atomic():
            if form.is_valid() and dish_formset.is_valid():
                self.object = form.save()
                dish_formset.instance = self.object
                dish_formset.save()
        return super(CreateView, self).form_valid(form)


class OrderUpdateView(OrderMixin, UpdateView):
    form_class = OrderForm
    pk_url_kwarg = 'order_id'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        context['dish_formset'] = DishFormSet(self.request.POST or None,
                                              instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        dish_formset = context['dish_formset']
        with transaction.atomic():
            if form.is_valid() and dish_formset.is_valid():
                form.save()
                dish_formset.save()
        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(OrderMixin, DeleteView):
    pk_url_kwarg = 'order_id'


class CategoryDetailView(DetailView):
    model = Category
    slug_url_kwarg = 'category_slug'
