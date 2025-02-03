from django.urls import path

from orders import views

app_name = 'orders'


urlpatterns = [
    path('', views.HomePage.as_view(), name='index'),
    path('orders/', views.OrderListView.as_view(), name='list'),
    path('orders/create/', views.OrderCreateView.as_view(), name='create'),
    path(
        'orders/<int:order_id>/edit/',
        views.OrderUpdateView.as_view(),
        name='edit'
    ),
    path(
        'orders/<int:order_id>/delete/',
        views.OrderDeleteView.as_view(),
        name='delete'
    ),
]
