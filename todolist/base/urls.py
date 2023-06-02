from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser,name='login'),
    path('register/', views.register,name='register'),
    path('logout/', views.logoutUser,name='logout'),
    path('', views.home,name='home'),
    path('create-task/', views.createTask,name='create-task'),
    path('update-task/<int:pk>/', views.updateTask,name='update-task'),
    path('delete-task/<int:pk>/', views.deleteTask,name='delete-task'),
]