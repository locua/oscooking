from django.contrib import admin
from django.urls import path,include
from . import views
from .views import *

app_name='recipes'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('allrecipes', views.AllRecipeView.as_view(), name='allrecipes'),
    path('alltags', views.AllTagView.as_view(), name='alltags'),
    path('submit/', views.submit_recipe_view, name='submit_rec'),
    path('donate/', views.donate_view, name='donate'),
    path('donationthanks/', views.donate_thanks_view, name='donationthanks'),
    path('thanks/', views.thanks, name='thanks'),
    path('recipes/<slug:recipe_slug>/', views.detail_view, name='detail'),
    path('tags/<slug:slug>/', views.tag_view, name='tag'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
]
