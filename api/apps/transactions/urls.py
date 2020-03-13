from django.urls import path

from api.apps.transactions.views import TransactionListCreateAPIView, TransactionDetailsView

urlpatterns = [
    path('transactions/', TransactionListCreateAPIView.as_view(), name='transactions-list-create'),
    path('transactions/<int:pk>', TransactionDetailsView.as_view(), name='transaction-details'),
]
