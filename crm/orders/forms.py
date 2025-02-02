from django import forms


from orders.models import Dish, Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'id',
            'table_number',
            'items',
            'status'
        )
