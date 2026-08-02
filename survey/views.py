from collections import Counter
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, TemplateView, View, ListView
from django.views.generic import ListView # <- PRECISA TER ISSO NO TOPO
from django.urls import reverse_lazy
from .models import PesquisaGravatai
from .forms import PesquisaForm
from .tasks import enviar_email_task

# Campos de escolha unica exibidos como ranking no dashboard
RANKED_FIELDS = [
    ('voto_presidente', 'Presidência'),
    ('voto_senador', 'Senado'),
    ('candidato_governador', 'Governo do Estado'),
    ('candidato_voto_hoje', 'Deputado (voto hoje)'),
    ('rumo_governo_estado', 'Rumo do Governo do Estado'),
    ('regiao_residencia', 'Região de residência'),
    ('sexo', 'Sexo'),
    ('faixa_etaria', 'Faixa etária'),
    ('escolaridade', 'Escolaridade'),
    ('ocupacao', 'Ocupação'),
    ('renda_familiar', 'Renda familiar'),
]

# Campos de multipla escolha (salvos como string separada por ", ")
MULTI_VALUE_FIELDS = [
    ('candidatos_poderia_votar', 'Candidatos considerados (Deputado)'),
    ('candidatos_rejeicao', 'Candidatos rejeitados (Deputado)'),
]

ZAFFALLON_ORDER = ['Ótima', 'Boa', 'Regular', 'Ruim', 'Péssima', 'Não sei']
ZAFFALLON_STATUS = {
    'Ótima': 'good',
    'Boa': 'good',
    'Regular': 'warning',
    'Ruim': 'serious',
    'Péssima': 'critical',
    'Não sei': 'neutral',
}

class SurveyView(CreateView):
    model = PesquisaGravatai
    form_class = PesquisaForm
    template_name = 'survey.html'
    success_url = reverse_lazy('survey_success')

    def form_valid(self, form):
        print("✅ SUCESSO! Formulário válido. Salvando...")
        response = super().form_valid(form)
        enviar_email_task.delay(form.cleaned_data)
        return response


    # ADICIONE ISTO AQUI PARA VER O ERRO:
    def form_invalid(self, form):
        print("❌ ERRO NO FORMULÁRIO!")
        print(form.errors)  # Vai imprimir no terminal qual campo está travando
        return super().form_invalid(form)


class SuccessView(TemplateView):
    template_name = 'success.html'

@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard_pro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = PesquisaGravatai.objects.all()
        total = qs.count()
        context['total_respostas'] = total

        hoje = timezone.localdate()
        context['respostas_hoje'] = qs.filter(created_at__date=hoje).count()
        context['respostas_7_dias'] = qs.filter(created_at__gte=timezone.now() - timedelta(days=7)).count()
        ultima = qs.order_by('-created_at').first()
        context['ultima_resposta'] = ultima.created_at if ultima else None
        context['ultimas_respostas'] = qs.order_by('-created_at')[:8]

        rankings = {}
        for field, label in RANKED_FIELDS:
            rows = (
                qs.exclude(**{f'{field}__isnull': True})
                  .exclude(**{field: ''})
                  .values(field)
                  .annotate(total=Count('id'))
                  .order_by('-total')
            )
            items = [
                {
                    'label': row[field],
                    'total': row['total'],
                    'pct': round(row['total'] / total * 100, 1) if total else 0,
                }
                for row in rows
            ]
            rankings[field] = {'label': label, 'items': items}

        for field, label in MULTI_VALUE_FIELDS:
            counter = Counter()
            for value in qs.exclude(**{field: ''}).values_list(field, flat=True):
                for item in (value or '').split(','):
                    item = item.strip()
                    if item:
                        counter[item] += 1
            items = [
                {'label': k, 'total': v, 'pct': round(v / total * 100, 1) if total else 0}
                for k, v in counter.most_common()
            ]
            rankings[field] = {'label': label, 'items': items}

        context['rankings'] = rankings

        zaff_counts = dict(
            qs.exclude(avaliacao_zaffallon__isnull=True)
              .exclude(avaliacao_zaffallon='')
              .values_list('avaliacao_zaffallon')
              .annotate(total=Count('id'))
        )
        context['avaliacao_zaffallon'] = [
            {
                'label': label,
                'total': zaff_counts[label],
                'pct': round(zaff_counts[label] / total * 100, 1) if total else 0,
                'status': ZAFFALLON_STATUS.get(label, 'neutral'),
            }
            for label in ZAFFALLON_ORDER if label in zaff_counts
        ]

        timeline = (
            qs.annotate(dia=TruncDate('created_at'))
              .values('dia').annotate(total=Count('id')).order_by('dia')
        )
        context['timeline_labels'] = [t['dia'].strftime('%d/%m') for t in timeline]
        context['timeline_values'] = [t['total'] for t in timeline]

        return context