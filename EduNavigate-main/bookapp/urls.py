from django.urls import path
from . import views
from .views import recommend_category
from .views import  summarise_pdf
urlpatterns = [
    path('home', views.home, name = 'home'),
    path('all_books', views.all_books, name = 'all_books'),
    path('genre/<str:slug>', views.category_detail, name = 'category_detail'),
    path('pdf/<str:slug>', views.book_detail, name = 'book_detail'),
    path('searched_books', views.search_book, name = 'book_search'),
    path('register', views.register_page, name = 'register'),
    path('login', views.login_page, name = 'login'),
    path('logout', views.logout_user, name = 'logout'),
    path('recommend_category', views.recommend_category, name = 'recommendation'),
    path('genre/<str:slug>/', views.cat_detail, name='cat_detail'),
    path('recommend_category', views.recommend_starting, name='recommend_starting'),
    path('summarise_pdf/', views.summarise_pdf, name='summarise_pdf'),
    
]