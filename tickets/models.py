from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration = models.IntegerField(help_text="Duration in minutes")
    description = models.TextField()
    release_date = models.DateField()
    poster = models.ImageField(upload_to='images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="movies")
    
    def __str__(self):
        return self.title

class Session(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    num_seats = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sessions")

    def __str__(self):
        return f"{self.movie.title} ({self.start_time} to {self.end_time})"

class Seat(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)
    is_occupied = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="seats")

    def __str__(self):
        status = "Occupied" if self.is_occupied else "Available"
        return f"Seat {self.seat_number} - {status}"
