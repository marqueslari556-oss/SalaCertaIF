# views.py - VERSÃO CORRIGIDA
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pessoa

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        
        try:
            pessoa = Pessoa.objects.get(email=email)
            
            # CORREÇÃO: Usar o método verificar_senha do model
            if pessoa.verificar_senha(senha):
                request.session['pessoa_id'] = pessoa.id
                request.session['pessoa_nome'] = pessoa.nome
                messages.success(request, f'Bem-vindo, {pessoa.nome}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Senha incorreta!')
                
        except Pessoa.DoesNotExist:
            messages.error(request, 'Usuário não encontrado! Contate o coordenador.')
        
        return redirect('login')
    
    return render(request, 'login.html')

def dashboard(request):
    if not request.session.get('pessoa_id'):
        messages.error(request, 'Faça login primeiro!')
        return redirect('login')
    
    context = {
        'nome': request.session.get('pessoa_nome'),
        'ocupacao': request.session.get('pessoa_ocupacao'),
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    request.session.flush()
    messages.success(request, 'Logout realizado com sucesso!')
    return redirect('login')