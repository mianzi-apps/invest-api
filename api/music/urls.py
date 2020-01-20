# urls.py file in the posts folder
from django.urls import path
from .views import ListSongsView, LoginView

urlpatterns = [
    path('songs/', ListSongsView.as_view(), name="songs-all"),
    path('auth/login', LoginView.as_view(), name="auth-login")
]
