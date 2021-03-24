from django.contrib import admin
from django.urls import path,include
from . import views

app_name='recipes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('submit/', views.submit_recipe_view, name='submit_rec'),
    path('<int:pk>/', views.detail_view, name='detail'),
]
