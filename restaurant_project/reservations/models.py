from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator

User = get_user_model()

class Table(models.Model):
    TABLE_TYPES = (
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('private', 'Private Room'),
    )
    
    number = models.CharField(max_length=10, unique=True)
    capacity = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    table_type = models.CharField(max_length=20, choices=TABLE_TYPES, default='indoor')
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Table {self.number} ({self.capacity} people)"

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField()
    reservation_time = models.TimeField()
    party_size = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(20)])
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['reservation_date', 'reservation_time']
        unique_together = ['table', 'reservation_date', 'reservation_time']

    def __str__(self):
        return f"Reservation for {self.user.username} on {self.reservation_date} at {self.reservation_time}"

    @property
    def is_upcoming(self):
        from django.utils import timezone
        from datetime import datetime, date
        reservation_datetime = datetime.combine(self.reservation_date, self.reservation_time)
        return reservation_datetime > timezone.now()