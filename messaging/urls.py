from django.urls import path
from messaging import views

urlpatterns = [
    path('', views.inbox, name='inbox'),
    path('start/<int:item_id>/', views.start_chat, name='start_chat'),
    path('room/<int:conv_id>/', views.room, name='room'),
]