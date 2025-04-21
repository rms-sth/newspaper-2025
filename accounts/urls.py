from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm # Import the custom login form

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', authentication_form=LoginForm), name='login'), # Use custom form
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), # Default template or redirect handled by settings
    path('register/', views.register, name='register'),
]