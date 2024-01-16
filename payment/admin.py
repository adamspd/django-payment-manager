from django.contrib import admin

from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'order_id',
        'reference_id',
        'amount',
        'currency',
        'status',
        'linked_object',
        'created_at',
        'updated_at'
    )
    search_fields = ('order_id', 'reference_id', 'status')
    list_filter = ('currency', 'status', 'created_at', 'updated_at')
