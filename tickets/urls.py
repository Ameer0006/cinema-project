from django.urls import path
from .views import (home_page, movie_details, session_list, session_details, book_seat, add_movie, edit_movie, delete_movie, add_session)

urlpatterns = [
    path('', home_page, name='home_page'),
    path('movies/add/', add_movie, name='add_movie'),
    path('movies/<int:pk>/', movie_details, name='movie_details'),
    path('movies/<int:pk>/edit/', edit_movie, name='edit_movie'),
    path('movies/<int:pk>/delete/', delete_movie, name='delete_movie'),
    path('sessions/<int:movie_id>/add/', add_session, name='add_session'),
    path('sessions/<int:movie_id>/', session_list, name='session_list'),
    path('sessions/<int:pk>/', session_details, name='session_details'),
    path('sessions/<int:session_id>/book/', book_seat, name='book_seat'),
]
