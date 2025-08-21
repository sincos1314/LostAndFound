from django.shortcuts import render
from items.models import Item

def home(request):
    latest = Item.objects.order_by('-created_at')[:8]
    return render(request, 'home.html', {'latest': latest})