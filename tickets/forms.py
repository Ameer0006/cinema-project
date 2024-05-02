from django import forms
from .models import Movie, Session, Seat

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'duration', 'description', 'release_date', 'poster']

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['movie', 'start_time', 'end_time', 'num_seats']

class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ['session', 'seat_number', 'is_occupied']