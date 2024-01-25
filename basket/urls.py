from django.urls import path
from .views import *

urlpatterns = [
    path('', basket_info, name='list_basket_product'),
    path('add/<int:product_id>', basket_add, name='add_basket_product'),
    path('remove/<int:product_id>', basket_remove, name='remove_basket_product'),
    path('clear/', basket_clear, name='clear_basket_product'),
]