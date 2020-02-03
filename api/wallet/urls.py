from django.urls import path
from .views import WalletDetailsView, WalletListView

urlpatterns = [
    path('wallet', WalletListView.as_view(), name='wallet-list-create'),
    path('wallet/<int:pk>', WalletDetailsView.as_view(), name='wallet-details'),
]
