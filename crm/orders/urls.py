from django.urls import path

from orders import views

urlpatterns = [
    path('', views.HomePage.as_view(), name='index')
]
