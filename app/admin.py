from django.contrib import admin
from django.contrib import messages
from django.utils.translation import ngettext
from .models import *
from django.contrib.admin import ModelAdmin

class PessoaAdmin(ModelAdmin):
    list_display = ('nome', 'email', 'cpf', 'ocupacao')
    search_fields = ('nome', 'email', 'cpf')
    list_filter = ('ocupacao',)
    
    def save_model(self, request, obj, form, change):
        # Se a senha foi fornecida e é diferente da já salva
        if 'senha_hash' in form.changed_data:
            senha_raw = form.cleaned_data.get('senha_hash')
            if senha_raw:
                obj.set_senha(senha_raw)  # Aplica o hash
        super().save_model(request, obj, form, change)
    
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if 'senha_hash' in fields:
            # Renomeia o campo no formulário para ficar mais amigável
            return fields
        return fields
    
    fieldsets = (
        ('Dados Pessoais', {
            'fields': ('nome', 'cpf', 'email', 'ocupacao')
        }),
        ('Senha', {
            'fields': ('senha_hash',),
            'description': 'Digite a senha em texto puro (será criptografada automaticamente)'
        }),
    )

# Registrar todos os modelos
admin.site.register(Ocupacao)
admin.site.register(Pessoa, PessoaAdmin)  # Use a classe personalizada
admin.site.register(Disciplina)
admin.site.register(Curso)
admin.site.register(Turma)
admin.site.register(AlocacaoProfessor)
admin.site.register(Horario)
admin.site.register(Sala)
admin.site.register(EquipamentoSala)
admin.site.register(SoftwareLaboratorio)
admin.site.register(StatusReserva)
admin.site.register(ReservaSala)
admin.site.register(TipoConflito)
admin.site.register(ConflitoReserva)
admin.site.register(TipoConservacao)
admin.site.register(TipoSala)