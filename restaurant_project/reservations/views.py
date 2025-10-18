from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import datetime, date, time
from .models import Reservation, Table
from .forms import ReservationForm

@login_required
def make_reservation(request):
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            
            # Find available table
            reservation_date = form.cleaned_data['reservation_date']
            reservation_time = form.cleaned_data['reservation_time']
            party_size = form.cleaned_data['party_size']
            
            # Find available table for the given time and party size
            available_tables = Table.objects.filter(
                is_available=True,
                capacity__gte=party_size
            ).exclude(
                reservations__reservation_date=reservation_date,
                reservations__reservation_time=reservation_time,
                reservations__status__in=['pending', 'confirmed']
            )
            
            if available_tables.exists():
                reservation.table = available_tables.first()
                reservation.save()
                messages.success(request, 'Reservation created successfully!')
                return redirect('reservation_history')
            else:
                messages.error(request, 'No tables available for the selected date and time. Please try a different time.')
    else:
        form = ReservationForm()
    
    return render(request, 'reservations/make_reservation.html', {'form': form})

@login_required
def reservation_history(request):
    reservations = Reservation.objects.filter(user=request.user).order_by('-reservation_date', '-reservation_time')
    return render(request, 'reservations/reservation_history.html', {'reservations': reservations})

@login_required
def reservation_detail(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if reservation.status in ['pending', 'confirmed'] and reservation.is_upcoming:
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, 'Reservation cancelled successfully!')
    else:
        messages.error(request, 'Cannot cancel this reservation.')
    
    return redirect('reservation_history')