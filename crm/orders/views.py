from django.db import transaction
from django.db.models import F, Sum, Q
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DeleteView, DetailView, ListView,
                                  TemplateView, UpdateView)


from orders.forms import DishFormSet, OrderForm
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


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    success_url = reverse_lazy('orders:list')
    self.object = None

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


class OrderUpdateView(OrderEditMixin, UpdateView):
    form_class = OrderForm

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


class OrderDeleteView(OrderEditMixin, DeleteView):
    pass
