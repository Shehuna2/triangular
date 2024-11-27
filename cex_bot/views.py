from django.shortcuts import render
from .models import ArbitrageOpportunity

def dashboard(request):
    """Render dashboard with arbitrage opportunities."""
    opportunities = ArbitrageOpportunity.objects.all()
    return render(request, 'dashboard.html', {'opportunities': opportunities})
