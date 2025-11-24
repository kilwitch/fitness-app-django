from . import views
from django.urls import path

urlpatterns = [
    path('',views.index, name='index'),
    path('track/', views.track_list, name='track_list'),
    path('create/',views.track_create, name='track_create'),
    path('<int:pk>/edit/',views.track_edit, name='track_edit'),
    path('<int:pk>/delete/',views.track_delete, name='track_delete'),
    path('profile/',views.profile_view, name='profile_view'),
    path('profile/create/',views.profile_create, name='profile_create'),
    path('profile/edit/',views.profile_edit, name='profile_edit'),
    path('profile/delete/',views.profile_delete, name='profile_delete'),
    path('register/',views.register,name='register'),
    path("charts/", views.charts_view, name="charts"),
     path("api/chat/", views.chat_api, name="chat_api"),
    path("chat/", views.chatbot_page, name="chat_page"),
] 
