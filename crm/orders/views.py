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


class OrderDeleteView(OrderEditMixin, DeleteView):
    template_name = 'orders/order_form.html'


class OrderUpdateView(OrderEditMixin, UpdateView):
    form_class = OrderForm
    template_name = 'orders/order_form.html'

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['dish_formset'] = DishFormSet(self.request.POST,
                                                  instance=self.object)
        else:
            context['dish_formset'] = DishFormSet(instance=self.object)

        return context


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:list')

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        dish_form = DishFormSet()
        return self.render_to_response(
            self.get_context_data(order_form=form,
                                  dish_formset=dish_form))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        dish_form = DishFormSet(self.request.POST)
        if form.is_valid() and dish_form.is_valid():
            return self.form_valid(form, dish_form)
        else:
            return self.form_invalid(form, dish_form)

    def form_valid(self, form, dish_form):
        self.object = form.save()
        dish_form.instance = self.object
        dish_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def from_invalid(self, form, dish_form):
        return self.render_to_response(
            self.get_context_data(order_form=form,
                                  dish_formset=dish_form))


# def create_order(request):
#     if request.method == 'POST':
#         order_form = OrderForm(request.POST)
#         dish_formset = DishFormSet(request.POST, prefix='Блюда')
#
#         if order_form.is_valid() and dish_formset.is_valid():
#             order = order_form.save()
#             dishes = dish_formset.save(commit=False)
#             for dish in dishes:
#                 dish.order = order
#                 dish.save()
#             return redirect('orders:list')
#     else:
#         order_form = OrderForm()
#         dish_formset = DishFormSet(prefix='Блюда')
#
#     return render(request, 'orders/order_form.html', {
#         'order_form': order_form,
#         'dish_formset': dish_formset
#     })