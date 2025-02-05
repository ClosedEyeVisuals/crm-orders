from django import forms


from orders.models import DishOrder, Order


class StatusForm(forms.Form):
    status = forms.ChoiceField(label='Статус',
                               choices=Order.OrderStatus.choices)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'id',
            'table_number',
            'status'
        )


class DishForm(forms.ModelForm):
    class Meta:
        model = DishOrder
        fields = (
            'dish',
            'amount'
        )


DishFormSet = forms.inlineformset_factory(
    Order,
    DishOrder,
    form=DishForm,
    extra=1,
    can_delete=False
)
