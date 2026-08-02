from django.contrib import admin, messages
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.html import format_html

from .admin_site import virtu_admin_site
from .models import Answer, PesquisaGravatai, Question, QuestionOption
from .tasks import enviar_email_task


class QuestionOptionInline(admin.TabularInline):
    model = QuestionOption
    extra = 1
    fields = ('order', 'label', 'value', 'status')
    ordering = ('order', 'id')


@admin.register(Question, site=virtu_admin_site)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('order', 'label', 'key', 'category', 'question_type', 'is_required', 'is_active', 'is_system')
    list_display_links = ('label',)
    list_editable = ('order', 'is_required', 'is_active')
    list_filter = ('question_type', 'is_active', 'category')
    search_fields = ('label', 'key')
    ordering = ('order', 'id')
    inlines = [QuestionOptionInline]
    fields = (
        'label', 'key', 'category', 'help_text', 'question_type', 'order',
        'is_required', 'is_active', 'depends_on', 'depends_on_value',
    )

    def get_readonly_fields(self, request, obj=None):
        if obj and obj.is_system:
            return ('key', 'question_type')
        return ()

    def has_delete_permission(self, request, obj=None):
        if obj is not None and obj.is_system:
            return False
        return super().has_delete_permission(request, obj)


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    fields = ('question', 'value')
    readonly_fields = ('question', 'value')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(PesquisaGravatai, site=virtu_admin_site)
class PesquisaGravataiAdmin(admin.ModelAdmin):
    # Colunas que aparecem na tabela principal
    list_display = (
        'id',
        'nome',
        'whatsapp',
        'created_at',
        'reenviar_email_button',
    )

    # Barra de pesquisa
    search_fields = ('nome', 'whatsapp')

    # Ordenação decrescente (mais recentes primeiro)
    ordering = ('-id',)
    readonly_fields = ('created_at',)
    inlines = [AnswerInline]

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
            payload = {'Nome': pesquisa.nome, 'WhatsApp': pesquisa.whatsapp or '--'}
            for answer in pesquisa.answers.select_related('question').order_by('question__order'):
                payload[answer.question.label] = answer.value
            enviar_email_task.delay(payload)
            messages.success(request, f'E-mail da pesquisa "{pesquisa.nome}" reenviado para a fila.')
        return redirect(reverse('admin:survey_pesquisagravatai_changelist'))
