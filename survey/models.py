from django.db import models


class PesquisaGravatai(models.Model):
    # Opções
    SEXO_CHOICES = [('Masculino', 'Masculino'), ('Feminino', 'Feminino'), ('Outro', 'Outro')]
    FAIXA_ETARIA = [('16-24', '16 a 24 anos'), ('25-34', '25 a 34 anos'), ('35-44', '35 a 44 anos'),
                    ('45-59', '45 a 59 anos'), ('60+', '60 anos ou mais')]
    ESCOLARIDADE = [('Analfabeto', 'Analfabeto'), ('Fundamental', 'Fundamental'), ('Medio', 'Ensino Médio'),
                    ('Superior', 'Superior'), ('Pos', 'Pós-graduação')]
    OCUPACAO = [('CLT', 'CLT'), ('Autonomo', 'Autônomo'), ('Empresario', 'Empresário'),
                ('Servidor', 'Servidor Público'), ('Estudante', 'Estudante'),
                ('Desempregado', 'Desempregado/Aposentado')]
    RENDA = [('Ate 1', 'Até 1 SM'), ('1 a 2', '1 a 2 SM'), ('2 a 5', '2 a 5 SM'), ('5 a 10', '5 a 10 SM'),
             ('Mais 10', 'Mais de 10 SM'), ('NaoResponder', 'Não responder')]

    created_at = models.DateTimeField(auto_now_add=True)
    sexo = models.CharField(max_length=20, choices=SEXO_CHOICES)
    sexo_outro = models.CharField(max_length=100, blank=True, null=True)
    faixa_etaria = models.CharField(max_length=20, choices=FAIXA_ETARIA)
    escolaridade = models.CharField(max_length=50, choices=ESCOLARIDADE)
    ocupacao = models.CharField(max_length=50, choices=OCUPACAO)

    # Perguntas Eleitorais
    candidatos_poderia_votar = models.TextField(verbose_name="Poderia Votar")
    candidato_voto_hoje = models.CharField(max_length=100, verbose_name="Voto Hoje")
    candidatos_rejeicao = models.TextField(verbose_name="Rejeição")
    candidato_governador = models.CharField(max_length=100)

    renda_familiar = models.CharField(max_length=50, choices=RENDA)
    nome = models.CharField(max_length=150)
    whatsapp = models.CharField(max_length=20)

    def __str__(self):
        return self.nome