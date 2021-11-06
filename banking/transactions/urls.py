from django.urls import path

from .views import account_details, account_list, transaction_details, transaction_list

urlpatterns = [
    path("accounts/", account_list),
    path("accounts/<int:pk>/", account_details),
    path("transactions/", transaction_list),
    path("transactions/<int:pk>/", transaction_details)
]
