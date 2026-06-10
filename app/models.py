from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError


class Ocupacao(models.Model):
    nome = models.CharField(max_length=40, verbose_name="Nome da ocupação")
    pode_reservar = models.BooleanField(verbose_name="Pode reservar")
    precisa_aprovacao = models.BooleanField(verbose_name="Precisa de aprovação")

    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Ocupção"
        verbose_name_plural = "Ocupações"


class Pessoa(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome da pessoa")
    cpf = models.CharField(max_length=14, verbose_name="CPF", unique=True)
    email = models.CharField(max_length=50, verbose_name="E-mail", unique=True)
    ocupacao = models.ForeignKey(Ocupacao, on_delete=models.CASCADE, verbose_name="Ocupação")

    senha_hash = models.CharField(max_length=128, verbose_name="Senha", blank=True, null=True)

    def __str__(self):
        return f"{self.nome}, {self.email}"
    
    #AUTENTICAÇÃO -------------------------------------------------------------------
    
    def set_senha(self, senha_raw):
        self.senha_hash = make_password(senha_raw)

    def verificar_senha(self, senha_raw):
        return check_password(senha_raw, self.senha_hash)
    
    class Meta:
        verbose_name = "Pessoa"
        verbose_name_plural = "Pessoas"


class Disciplina(models.Model):
    nome = models.CharField(max_length=40, verbose_name="Disciplina")
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"


class Curso(models.Model):
    nome = models.CharField(max_length=40, verbose_name="Nome do curso")
    
    def __str__(self):
        return self.nome
    
    class Meta:
        verbose_name = "Curso"
        verbose_name_plural = "Cursos" 


class Turma(models.Model):
    turma = models.CharField(max_length=10, verbose_name="Turma")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name="Curso")
    
    def __str__(self):
        return self.turma
    
    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"


class AlocacaoProfessor(models.Model):
    ano_letivo = models.IntegerField(verbose_name="Ano letivo")
    semestre_letivo = models.IntegerField(verbose_name="Semestre letivo")
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Nome da pessoa")
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, verbose_name="Disciplina")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, verbose_name="Curso")
    
    def __str__(self):
        return f"{self.pessoa}, {self.turma}, {self.disciplina}"
    
    class Meta:
        verbose_name = "Alocação"
        verbose_name_plural = "Alocações"


class Horario(models.Model):
    dia_semana = models.CharField(max_length=20, verbose_name="Dia da semana")
    hora_inicio = models.TimeField(verbose_name="Horário de inicio")
    hora_fim = models.TimeField(verbose_name="Horário de fim")
    
    def __str__(self):
        return self.dia_semana
    
    class Meta:
        verbose_name = "Horário"
        verbose_name_plural = "Horários"

class TipoConservacao(models.Model):
    tipo_conservacao = models.CharField(max_length=30, verbose_name="Conservação")
    prioridade_manutencao = models.CharField(max_length=6, verbose_name="Nível de prioridade")
    
    def __str__(self):
        return self.tipo_conservacao
    
    class Meta:
        verbose_name = "Conservação"
        verbose_name_plural = "Conservações" 


class TipoSala(models.Model):
    tipo_sala = models.CharField(max_length=50, verbose_name="Tipo da sala")

    def __str__(self):
        return self.tipo_sala
    
    class Meta:
        verbose_name = "Tipo de Sala"
        verbose_name_plural = "Tipos de Sala"



class Sala(models.Model):
    numero = models.IntegerField(verbose_name="Número da sala")
    predio = models.CharField(max_length=30, verbose_name="Prédio")
    capacidade = models.IntegerField(verbose_name="Capacidade (pessoas)")
    tipo_sala = models.ForeignKey(TipoSala, on_delete = models.CASCADE, verbose_name="Tipo da sala")
    ativa = models.BooleanField(default=True, verbose_name="Sala ativa")
    
    def __str__(self):
        return f"{self.numero}, {self.tipo_sala}, {self.predio}"
    
    class Meta:
        verbose_name = "Sala"
        verbose_name_plural = "Salas"


class EquipamentoSala(models.Model):
    nome_equipamento = models.CharField(max_length=50, verbose_name="Nome do equipamento", default='Sem nome')
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name="Sala")
    quantidade = models.IntegerField(verbose_name="Quantidade de equipamentos")
    tipo_conservacao = models.ForeignKey(TipoConservacao, on_delete=models.CASCADE, verbose_name="Estado da conservação")
    
    def __str__(self):
        return self.nome_equipamento
    
    class Meta:
        verbose_name = "Equipamento"
        verbose_name_plural = "Equipamentos"


class SoftwareLaboratorio(models.Model):
    nome_software = models.CharField(max_length=50, verbose_name="Nome do software")
    versao = models.CharField(max_length=15, verbose_name="Versão do software")
    sistema_operacional = models.CharField(max_length=30, verbose_name="Sistema operacional")
    sala = models.ForeignKey('Sala', on_delete=models.CASCADE, verbose_name="Sala")

    def __str__(self):
        return f"{self.nome_software}, {self.sala}"

    class Meta:
        verbose_name = "Software por laboratório"
        verbose_name_plural = "Softwares por laboratório"


class StatusReserva(models.Model):
    nome = models.CharField(max_length=30, verbose_name="Status da reserva")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Status da reserva"
        verbose_name_plural = "Status das reservas"


class ReservaSala(models.Model):
    pessoa = models.ForeignKey(Pessoa, on_delete=models.CASCADE, verbose_name="Pessoa")
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, verbose_name="Sala")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, verbose_name="Horário")
    alocacao_professor = models.ForeignKey(AlocacaoProfessor, on_delete=models.CASCADE,verbose_name="Alocação do professor")
    status_reserva = models.ForeignKey(StatusReserva, on_delete= models.CASCADE, verbose_name = "Status da reserva")
    
    def __str__(self):
        return f"{self.sala}, {self.horario}"

    class Meta:
        verbose_name = "Reserva de sala"
        verbose_name_plural = "Reservas de salas"


class TipoConflito(models.Model):
    nome = models.CharField(max_length=50, verbose_name="Tipo de conflito")

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name = "Tipo de conflito"
        verbose_name_plural = "Tipos de conflito"


class ConflitoReserva(models.Model):
    reserva = models.ForeignKey(ReservaSala, on_delete=models.CASCADE, verbose_name="Reserva")
    descricao = models.CharField(max_length=80, verbose_name="Descrição do conflito")
    resolvido = models.BooleanField(default=False, verbose_name="Resolvido")
    tipo_conflito = models.ForeignKey(TipoConflito, on_delete=models.CASCADE, verbose_name="Tipo de conflito")

    def __str__(self):
        return f"Conflito: {self.reserva} - {self.tipo_conflito}"

    class Meta:
        verbose_name = "Conflito de reserva"
        verbose_name_plural = "Conflitos de reservas"