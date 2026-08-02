from django.contrib import admin, messages
from django.forms.models import model_to_dict
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .models import PesquisaGravatai
from .tasks import enviar_email_task

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
        'avaliacao_zaffallon',
        'reenviar_email_button',
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

    def reenviar_email_button(self, obj):
        url = reverse('admin:survey_pesquisagravatai_reenviar_email', args=[obj.pk])
        return format_html('<a class="button" href="{}">Reenviar e-mail</a>', url)
    reenviar_email_button.short_description = 'E-mail'

    def get_urls(self):
        custom_urls = [
            path(
                '<int:pk>/reenviar-email/',
                self.admin_site.admin_view(self.reenviar_email_view),
                name='survey_pesquisagravatai_reenviar_email',
            ),
        ]
        return custom_urls + super().get_urls()

    def reenviar_email_view(self, request, pk):
        pesquisa = self.get_object(request, pk)
        if pesquisa is None:
            messages.error(request, 'Pesquisa não encontrada.')
        else:
            enviar_email_task.delay(model_to_dict(pesquisa))
            messages.success(request, f'E-mail da pesquisa "{pesquisa.nome}" reenviado para a fila.')
        return redirect(reverse('admin:survey_pesquisagravatai_changelist'))