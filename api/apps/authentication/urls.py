# urls.py file in the posts folder
from django.urls import path
from api.apps.authentication.views import LoginView, RegisterView

urlpatterns = [
    path('auth/login', LoginView.as_view(), name='auth-login'),
    path('auth/register', RegisterView.as_view(), name='auth-register')
]
