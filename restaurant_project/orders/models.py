from django.db import models
from django.contrib.auth import get_user_model
from menu.models import MenuItem

User = get_user_model()

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart of {self.user.username}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'menu_item']

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    @property
    def total_price(self):
        return self.menu_item.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('ready', 'Ready for Pickup'),
        ('served', 'Served'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    DELIVERY_TYPE_CHOICES = (
        ('takeaway', 'Takeaway'),
        ('dine_in', 'Dine In'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    order_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    delivery_type = models.CharField(max_length=20, choices=DELIVERY_TYPE_CHOICES, default='dine_in')
    delivery_address = models.TextField(blank=True, help_text="Required for takeaway orders")
    table_number = models.CharField(max_length=10, blank=True, help_text="Required for dine-in orders")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    special_instructions = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.order_number} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            last_id = last_order.id if last_order else 0
            self.order_number = f"ORD{last_id + 1:06d}"
        super().save(*args, **kwargs)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    special_instructions = models.TextField(blank=True)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"

    @property
    def total_price(self):
        return self.price * self.quantity