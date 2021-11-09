from rest_framework import serializers

from .models import Account, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'


class AccountTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["cashAmount", "destinationAccount"]

    def validate_cashAmount(self, value):
        sourceAccount = self.initial_data['sourceAccount']

        if sourceAccount.availableCash < value:
            raise serializers.ValidationError("You can't transfer more cash than you have.")
        return value


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'