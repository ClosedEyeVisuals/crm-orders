from django import forms


from orders.models import DishOrder, Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = (
            'id',
            'table_number',
            # 'items',
            'status'
        )


class DishForm(forms.ModelForm):
    class Meta:
        model = DishOrder
        fields = (
            'dish',
            'amount'
        )


DishFormSet = forms.inlineformset_factory(Order, DishOrder,
                                          form=DishForm, extra=1, can_delete=False)
