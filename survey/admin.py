from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PesquisaGravatai


@admin.register(PesquisaGravatai)
class PesquisaGravataiAdmin(admin.ModelAdmin):
    # Colunas que aparecem na tabela
    list_display = ('id', 'nome', 'whatsapp', 'regiao_residencia', 'voto_presidente', 'avaliacao_zaffallon')

    # Filtros laterais para cruzar dados rápido (ex: ver só quem vota Zema e acha o governo Ótimo)
    list_filter = ('regiao_residencia', 'voto_presidente', 'rumo_governo_estado', 'avaliacao_zaffallon')

    # Barra de pesquisa
    search_fields = ('nome', 'whatsapp')

    # Ordenação decrescente (mais recentes primeiro)
    ordering = ('-id',)