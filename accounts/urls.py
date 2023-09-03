from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from .views import *

urlpatterns = [

    path('profile/', UserProfile.as_view(), name='profile'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('signup/', SingUpView.as_view(), name='signup'),
    path('signup_mail_sent/', signup_mail_sent_view, name='signup_mail_sent'),
    path('<int:pk>/confirmation_signup/', ConfirmationSignUp.as_view(), name='conf_signup'),

]