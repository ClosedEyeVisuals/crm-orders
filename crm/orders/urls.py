from django.urls import path

from orders import views

app_name = 'orders'

urlpatterns = [
    path('', views.HomePage.as_view(), name='index')
]
