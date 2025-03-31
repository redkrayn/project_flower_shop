from django.contrib import admin
from .models import *


class OrderAdmin(admin.ModelAdmin):
    list_display = ('flower_name', 'customer', 'order_status', 'delivery_date', 'order_price')


admin.site.register(Bouquet)
admin.site.register(Customer)
admin.site.register(Order, OrderAdmin)
