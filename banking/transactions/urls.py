from django.urls import path

from .views import account_details, account_list, transaction_details, transaction_list, withdraw_action

urlpatterns = [
    path("accounts/", account_list),
    path("accounts/<int:pk>/", account_details),
    path("accounts/<int:pk>/withdraw", withdraw_action),
    path("transactions/", transaction_list),
    path("transactions/<int:pk>/", transaction_details)
]
