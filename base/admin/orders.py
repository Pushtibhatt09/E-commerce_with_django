from django.contrib import admin
from base.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'payment_status', 'created_at')
    search_fields = ('user__email', 'id')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order_link', 'product', 'quantity', 'price')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')

    def order_link(self, obj):
        from django.urls import reverse
        from django.utils.html import format_html
        url = reverse('admin:base_order_change', args=[obj.order.id])
        return format_html('<a href="{}">{}</a>', url, obj.order.id)

    order_link.short_description = 'Order'
    order_link.admin_order_field = 'order'
