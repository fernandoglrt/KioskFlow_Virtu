from collections import Counter
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import FormView, TemplateView

from .dedup import is_recent_duplicate
from .forms import build_skip_rules, build_survey_form
from .models import Answer, PesquisaGravatai, Question
from .tasks import enviar_email_task


class SurveyView(FormView):
    template_name = 'survey.html'
    success_url = reverse_lazy('survey_success')

    def get_form(self, form_class=None):
        return build_survey_form(data=self.request.POST or None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['skip_rules'] = build_skip_rules()
        return context

    def form_valid(self, form):
        cleaned = dict(form.cleaned_data)
        response = PesquisaGravatai.objects.create(
            nome=(cleaned.pop('nome', '') or '').strip(),
            whatsapp=cleaned.pop('whatsapp', '') or None,
        )

        questions_by_key = {q.key: q for q in Question.objects.filter(key__in=cleaned.keys())}
        answers = []
        email_payload = {}
        for key, value in cleaned.items():
            question = questions_by_key.get(key)
            if question is None or not value:
                continue
            stored = ', '.join(value) if isinstance(value, list) else str(value)
            answers.append(Answer(response=response, question=question, value=stored))
            email_payload[question.label] = stored
        Answer.objects.bulk_create(answers)

        if is_recent_duplicate(response):
            response.is_duplicate = True
            response.save(update_fields=['is_duplicate'])
        else:
            enviar_email_task.delay(email_payload)
        return super().form_valid(form)

    def form_invalid(self, form):
        print("❌ ERRO NO FORMULÁRIO!")
        print(form.errors)
        return super().form_invalid(form)


class SuccessView(TemplateView):
    template_name = 'success.html'


@method_decorator(staff_member_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'dashboard_pro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        responses = PesquisaGravatai.objects.filter(is_duplicate=False)
        total = responses.count()
        context['total_respostas'] = total
        context['total_duplicatas'] = PesquisaGravatai.objects.filter(is_duplicate=True).count()

        hoje = timezone.localdate()
        context['respostas_hoje'] = responses.filter(created_at__date=hoje).count()
        context['respostas_7_dias'] = responses.filter(created_at__gte=timezone.now() - timedelta(days=7)).count()
        ultima = responses.order_by('-created_at').first()
        context['ultima_resposta'] = ultima.created_at if ultima else None

        recent = list(responses.order_by('-created_at')[:8])
        regiao_by_response = dict(
            Answer.objects.filter(question__key='regiao_residencia', response__in=recent)
            .values_list('response_id', 'value')
        )
        context['ultimas_respostas'] = [
            {
                'nome': r.nome,
                'whatsapp': r.whatsapp,
                'regiao': regiao_by_response.get(r.id, ''),
                'created_at': r.created_at,
            }
            for r in recent
        ]

        status_sections = []
        category_order = []
        charts_by_category = {}
        chart_seq = 0

        questions = (
            Question.objects.filter(is_active=True, is_system=False)
            .prefetch_related('options')
            .order_by('order', 'id')
        )
        for question in questions:
            answers_qs = Answer.objects.filter(question=question, response__is_duplicate=False).exclude(value='')
            counter = Counter()
            if question.question_type == Question.CHECKBOX_MULTI:
                for value in answers_qs.values_list('value', flat=True):
                    for item in value.split(','):
                        item = item.strip()
                        if item:
                            counter[item] += 1
            else:
                for row in answers_qs.values('value').annotate(total=Count('id')):
                    counter[row['value']] = row['total']

            options = list(question.options.all())
            status_by_value = {opt.effective_value: opt.status for opt in options if opt.status}
            is_status_question = bool(status_by_value) and all(v in status_by_value for v in counter)

            chart_seq += 1
            chart_id = f'chart-{chart_seq}'

            if is_status_question:
                items = []
                for opt in options:
                    v = opt.effective_value
                    if v in counter:
                        items.append({
                            'label': opt.label,
                            'total': counter[v],
                            'pct': round(counter[v] / total * 100, 1) if total else 0,
                            'status': opt.status or 'neutral',
                        })
                status_sections.append({'id': chart_id, 'label': question.label, 'items': items})
            elif counter:
                items = [
                    {'label': label, 'total': qty, 'pct': round(qty / total * 100, 1) if total else 0}
                    for label, qty in counter.most_common()
                ]
                category = question.category or 'Outras perguntas'
                if category not in charts_by_category:
                    charts_by_category[category] = []
                    category_order.append(category)
                charts_by_category[category].append({'id': chart_id, 'label': question.label, 'items': items})

        ranking_categories = [
            {'name': name, 'charts': charts_by_category[name]} for name in category_order
        ]
        context['ranking_categories'] = ranking_categories
        context['status_sections'] = status_sections
        context['chart_specs_json'] = (
            [{**s, 'kind': 'status'} for s in status_sections]
            + [{**c, 'kind': 'bar'} for cat in ranking_categories for c in cat['charts']]
        )

        timeline = (
            responses.annotate(dia=TruncDate('created_at'))
            .values('dia').annotate(total=Count('id')).order_by('dia')
        )
        context['timeline_labels'] = [t['dia'].strftime('%d/%m') for t in timeline]
        context['timeline_values'] = [t['total'] for t in timeline]

        return context
