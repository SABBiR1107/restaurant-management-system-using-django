from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from orders.models import Order

User = get_user_model()

class Feedback(models.Model):
    RATING_CHOICES = (
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='feedbacks', null=True, blank=True)
    rating = models.IntegerField(choices=RATING_CHOICES, validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'order']

    def __str__(self):
        return f"Feedback from {self.user.username} - Rating: {self.rating}"

    @property
    def rating_stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)