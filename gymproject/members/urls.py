from django.urls import path
from .views import register, member_list, dashboard, manage_users, create_user, member_detail, report

urlpatterns = [
    path('register/', register, name='register'),
    path('', member_list, name='member_list'),
    path('dashboard/', dashboard, name='dashboard'),
    path('users/', manage_users, name='manage_users'),
    path('users/add/', create_user, name='create_user'),
    path('member/<int:member_id>/', member_detail, name='member_detail'),
    path('report/', report, name='report'),
] 