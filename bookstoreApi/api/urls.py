from django.urls import path

from . import views

urlpatterns = [
    path('', views.welcome, name='index'),
    path('/books', views.get_books, name='books'),
    path('/<int:book_id>/book', views.get_book, name='book'),
    path('/new_book', views.input_book, name='input_book'),
    path('/categories', views.get_categories, name='categories'),
    path('/<int:book_id>/book/<int:chapter_id>/<int:subchapter_id>', views.get_page, name='page'),

]
