from django.shortcuts import render
from .models import Pessoa, Sala, ReservaSala

def index(request):
    context = {
        'total_pessoas': Pessoa.objects.count(),
        'total_salas': Sala.objects.count(),
        'total_reservas': ReservaSala.objects.count(),
    }
    return render(request, 'index.html', context)