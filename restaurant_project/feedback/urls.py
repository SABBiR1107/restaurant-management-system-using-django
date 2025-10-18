from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_feedback, name='submit_feedback'),
    path('submit/<int:order_id>/', views.submit_feedback, name='submit_feedback_with_order'),
    path('history/', views.feedback_history, name='feedback_history'),
]