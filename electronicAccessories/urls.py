from django.urls import path
from electronicAccessories.views import *

urlpatterns = [
    path('', index_template, name='laptop_index'),
    path('laptopsList/', laptops_template, name='laptop_list'),
    path('httpresponse/', index),
    path('laptopadd/', laptop_add, name='laptop_add'),
    path('laptopsList/<int:laptop_id>/', laptop_detail, name='one_laptop'),

    path('supplier/list/', supplier_list, name='list_supplier'),
    path('supplier/add/', supplier_base, name='add_supplier'),

    path('supplier/view/list/', Supplier_list_view.as_view(), name='list_supplier_view'),

    path('supplier/view/<int:supplier_id>', SupplierOneView.as_view(), name='info_supplier_view'),

    path('supplier/view/add/', Supplier_create_view.as_view(), name='add_supplier_view'),
    path('supplier/view/update/<int:pk>', Supplier_update_view.as_view(), name='update_supplier_view'),
    path('supplier/view/delete/<int:pk>', Supplier_delete_view.as_view(), name='delete_supplier_view'),

    path('laptop/<int:laptop_id>/update/', laptop_update, name='laptop_update'),
    path('laptop/<int:laptop_id>/delete/', laptop_delete, name='laptop_delete'),

    path('registr/', user_registration, name='registr'),
    path('auth/', user_authorization, name='auth'),
    path('logout/', user_logout, name='logout'),

    path('email/', send_email, name='send_email'),

    path('api/list/', laptops_api_list, name='laptops_api_list'),
    path('api/one/<int:pk>', laptop_api_one, name='laptops_api_one'),

]

