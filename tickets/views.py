from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Movie, Session, Seat
from .forms import MovieForm, SessionForm, SeatForm


def home_page(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all().order_by('-release_date')
        paginator = Paginator(movies, 10)  
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'tickets/index.html', {'page_obj': page_obj})
    else:
        return redirect('/auth/login/')

@login_required
def add_movie(request):
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.user = request.user
            movie.save()
            if 'submit' in request.POST and request.POST['submit'] == 'add_and_create_session':
                return redirect(reverse('add_session', kwargs={'movie_id': movie.id}))
            return redirect('home_page')
    else:
        form = MovieForm()
    return render(request, 'tickets/add_movie.html', {'form': form})


@login_required
def movie_details(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    return render(request, 'tickets/movie_details.html', {'movie': movie})

@login_required
def edit_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_details', pk=pk)
    else:
        form = MovieForm(instance=movie)
    return render(request, 'tickets/edit_movie.html', {'form': form, 'movie': movie})

@login_required
def delete_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    if request.user.is_authenticated and request.user == movie.user:
        if request.method == 'POST':
            movie.delete()
            return redirect('home_page')
        else:
            return redirect('movie_details', pk=pk)
    else:
        return redirect('home_page')

@login_required
def add_session(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.movie = movie
            session.user = request.user
            session.save()
            return redirect('session_list', movie_id=movie.id)
    else:
        form = SessionForm()
    return render(request, 'tickets/add_session.html', {'form': form, 'movie': movie})


def session_list(request, movie_id):
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        messages.error(request, "The movie with the specified ID does not exist.")
        return redirect('home_page')
    
    sessions = movie.session_set.all().order_by('start_time')
    return render(request, 'tickets/session_list.html', {'movie': movie, 'sessions': sessions})


def session_details(request, pk):
    session = get_object_or_404(Session, pk=pk)
    seats = session.seat_set.all()
    return render(request, 'tickets/session_details.html', {'session': session, 'seats': seats})

@login_required
def book_seat(request, session_id):
    session = get_object_or_404(Session, pk=session_id)
    seats = session.seat_set.all().order_by('seat_number')
    if request.method == 'POST':
        form = SeatForm(request.POST)
        if form.is_valid():
            seat = form.save(commit=False)
            seat.user = request.user
            seat.session = session
            seat.is_occupied = True
            seat.save()
            return redirect('session_details', pk=session.pk)
    else:
        form = SeatForm(initial={'session': session})
    return render(request, 'tickets/book_seat.html', { 'session': session, 'seats': seats, 'form': form})
