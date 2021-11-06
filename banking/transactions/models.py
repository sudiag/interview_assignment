from django.db import models


# Create your models here.
class Account(models.Model):
    name = models.CharField(max_length=200)
    availableCash = models.DecimalField(max_digits=12, decimal_places=2)


class Transaction(models.Model):
    registeredTime = models.DateTimeField(auto_now_add=True)
    executedTime = models.DateTimeField(null=True)
    success = models.BooleanField(null=True)
    cashAmount = models.DecimalField(max_digits=12, decimal_places=2) #change! inaccurate!
    sourceAccount = models.ForeignKey("Account", related_name="withdrawals", on_delete=models.RESTRICT)
    destinationAccount = models.ForeignKey("Account", related_name="debits", on_delete=models.RESTRICT)
