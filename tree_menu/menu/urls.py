from django.urls import path
from .views import menu_view, homepage_view

urlpatterns = [
    path('', homepage_view, name='main_menu'),
    path('<str:menu_name>/', menu_view, name='menu'),
]