import decimal

from django.shortcuts import render

# Create your views here.
from rest_framework import status, serializers
from rest_framework.decorators import api_view, action
from rest_framework.response import Response

from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, AccountTransactionSerializer

from django.db import transaction as atomic_transaction


@api_view(['GET', 'POST'])
def account_list(request):
    if request.method == "GET":
        accounts = Account.objects.all()
        serializer = AccountSerializer(accounts, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # redirect to account in question?
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def account_details(request, pk):
    try:
        account = Account.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = AccountSerializer(account)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def transaction_list(request):
    if request.method == "GET":
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # redirect to transaction in question?
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
def transaction_details(request, pk):
    try:
        transaction = Transaction.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = TransactionSerializer(transaction)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = TransactionSerializer(transaction, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def withdraw_action(request, pk):
    try:
        sourceAccount = Account.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AccountTransactionSerializer(data=request.data)
    serializer.initial_data['sourceAccount'] = sourceAccount
    if serializer.is_valid():
        destinationAccount = Account.objects.get(pk=serializer.data['destinationAccount'])

        sourceAccount.availableCash = sourceAccount.availableCash - decimal.Decimal(serializer.data['cashAmount'])
        destinationAccount.availableCash = destinationAccount.availableCash + decimal.Decimal(serializer.data['cashAmount'])

        transaction = Transaction(
            cashAmount=decimal.Decimal(serializer.data['cashAmount']),
            success=True,
            sourceAccount=sourceAccount,
            destinationAccount=destinationAccount,
        )

        with atomic_transaction.atomic():
            transaction.save()
            sourceAccount.save()
            destinationAccount.save()

        serializer = TransactionSerializer(transaction)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
