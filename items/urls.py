from django.urls import path
from items import views

urlpatterns = [
    path('', views.item_list, name='list'),
    path('create/', views.item_create, name='create'),
    path('<int:pk>/', views.item_detail, name='detail'),
    path('<int:pk>/edit/', views.item_edit, name='edit'),
]