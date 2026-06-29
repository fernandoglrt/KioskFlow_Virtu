from django.contrib import admin
from .models import PesquisaGravatai

@admin.register(PesquisaGravatai)
class PesquisaGravataiAdmin(admin.ModelAdmin):
    # Colunas que aparecem na tabela principal
    list_display = (
        'id',
        'nome',
        'whatsapp',
        'regiao_residencia',
        'voto_presidente',
        'voto_senador',
        'avaliacao_zaffallon'
    )

    # Filtros laterais para cruzamento de dados ágil
    list_filter = (
        'regiao_residencia',
        'voto_presidente',
        'voto_senador',
        'rumo_governo_estado',
        'avaliacao_zaffallon'
    )

    # Barra de pesquisa
    search_fields = ('nome', 'whatsapp')

    # Ordenação decrescente (mais recentes primeiro)
    ordering = ('-id',)