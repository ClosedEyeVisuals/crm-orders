import django_filters

from orders.models import Order


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Order
        fields = (
            'table_number',
            'status'
        )


class OrderDateRangeFilter(django_filters.FilterSet):
    created_at = django_filters.DateFromToRangeFilter(
        label='Период',
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'class': 'datepicker',
                'type': 'date'
            }
        )
    )

    class Meta:
        model = Order
        fields = (
            'created_at',
        )
