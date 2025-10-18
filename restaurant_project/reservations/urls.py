from django.urls import path
from . import views

urlpatterns = [
    path('make/', views.make_reservation, name='make_reservation'),
    path('history/', views.reservation_history, name='reservation_history'),
    path('detail/<int:reservation_id>/', views.reservation_detail, name='reservation_detail'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
]