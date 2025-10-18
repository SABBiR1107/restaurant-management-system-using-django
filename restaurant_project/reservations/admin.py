from django.contrib import admin
from .models import Table, Reservation

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'capacity', 'table_type', 'is_available', 'created_at')
    list_filter = ('table_type', 'is_available')
    search_fields = ('number', 'description')
    ordering = ('number',)

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('user', 'table', 'reservation_date', 'reservation_time', 'party_size', 'status', 'created_at')
    list_filter = ('status', 'reservation_date', 'table')
    search_fields = ('user__username', 'table__number', 'special_requests')
    ordering = ('reservation_date', 'reservation_time')
    autocomplete_fields = ['user', 'table']