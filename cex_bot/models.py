from django.db import models

class ArbitrageOpportunity(models.Model):
    path = models.CharField(max_length=255)
    profit = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
