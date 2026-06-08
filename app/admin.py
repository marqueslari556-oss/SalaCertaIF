from django.contrib import admin
from .models import *
from django.contrib import admin

admin.site.register(Ocupacao)
admin.site.register(Pessoa)
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
