from django.contrib import admin
from django.urls import path,include
from . import views

app_name='submit_recipe'
urlpatterns = [
    # ex: /news
    path('', views.submit_recipe_view, name='submit_rec'),
    #path('admin/', admin.sites.urls),
    # Below path is for use with detailview class
    # path('<int:pk>/', views.DetailView.as_view(), name='detail'), 
]
