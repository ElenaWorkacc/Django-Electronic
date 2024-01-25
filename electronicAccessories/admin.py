from django.contrib import admin
from .models import Electronic, Supplier, Order, Pos_order, Invoice

class ElectronicAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'supplier', 'exist')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'price')
    list_editable = ('price', 'exist')
    list_filter = ('exist', 'supplier')

admin.site.register(Electronic, ElectronicAdmin)

class SupplierAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'representative_firstname',
        'representative_lastname',
        'representative_patronymic',
        'exist'
    )

    list_display_links = ('id', 'title')
    search_fields = ('title', 'representative_lastname')
    list_editable = ('exist',)
    list_filter = ('exist',)

admin.site.register(Supplier, SupplierAdmin)

class Order_Admin(admin.ModelAdmin):
    list_display = ('id', 'date_create', 'date_finish', 'status', 'price', 'address')
    list_display_links = ('id', )
    search_fields = ('date_create', 'address')
    list_editable = ('date_finish', 'status')
    list_filter = ('status',)

admin.site.register(Order, Order_Admin)


class Pos_order_Admin(admin.ModelAdmin):
    list_display = ('id', 'laptop', 'order', 'count_laptop', 'price')
    list_display_links = ('laptop', 'order')
    search_fields = ('laptop', 'order')

admin.site.register(Pos_order, Pos_order_Admin)


class Invoice_Admin(admin.ModelAdmin):
    list_display = ('order', 'date_printout', 'address_printout', 'terminal')
    list_display_links = ('order', 'date_printout')
    search_fields = ('date_printout', 'address_printout')

admin.site.register(Invoice, Invoice_Admin)

