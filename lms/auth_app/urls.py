from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
   
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
     path('logout/', views.logout_view, name='logout'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]