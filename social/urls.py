from lib2to3.fixes.fix_asserts import NAMES

from  django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
app_name="social"

urlpatterns=[
    path('',views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name="login"),
    path('logout/', views.log_out, name="logout"),
    path('register/', views.register, name="register"),
    path('user/edit', views.edit_user, name="edit_account"),
    path('ticket', views.ticket, name="ticket"),
]