from django import forms
from .models import Reservation
from datetime import date, time
import datetime

class ReservationForm(forms.ModelForm):
    reservation_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': date.today()}),
        initial=date.today
    )
    reservation_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        initial=time(18, 0)  # 6:00 PM
    )

    class Meta:
        model = Reservation
        fields = ['reservation_date', 'reservation_time', 'party_size', 'special_requests']
        widgets = {
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_reservation_date(self):
        reservation_date = self.cleaned_data['reservation_date']
        if reservation_date < date.today():
            raise forms.ValidationError("Reservation date cannot be in the past.")
        return reservation_date

    def clean_party_size(self):
        party_size = self.cleaned_data['party_size']
        if party_size < 1:
            raise forms.ValidationError("Party size must be at least 1.")
        if party_size > 20:
            raise forms.ValidationError("Party size cannot exceed 20.")
        return party_size