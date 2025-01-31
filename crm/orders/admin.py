from django.contrib import admin
from django.db.models import F, Sum

from orders.models import Category, Dish, DishOrder, Order, Table


class DishInlines(admin.TabularInline):
    model = DishOrder
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
    )
    search_fields = (
        'title',
    )


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'price',
        'category'
    )
    list_filter = (
        'category',
    )


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (
        DishInlines,
    )
    list_display = (
        'created_at',
        'order_id',
        'status',
        'table_number',
        'dishes',
        'total_price'
    )
    list_editable = (
        'status',
    )
    list_filter = (
        'status',
    )
    list_display_links = (
        'created_at',
        'order_id',
    )
    search_fields = (
        'table_number__number',
        'status'
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.annotate(
            total_price=Sum(
                F('order_dishes__dish__price') * F('order_dishes__amount')
            )
        )

    @admin.display(description='номер заказа')
    def order_id(self, obj):
        return obj.id

    @admin.display(description='блюда в заказе')
    def dishes(self, obj):
        return [item.dish.title for item in obj.order_dishes.all()]

    @admin.display(description='сумма заказа')
    def total_price(self, obj):
        return obj.total_price
