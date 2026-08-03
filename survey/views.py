from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse_lazy
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
    """Manda os dados crus pro front (perguntas, respostas, respostas-a-perguntas)
    e deixa o JS calcular tudo (rankings, KPIs, filtros) no navegador — assim
    clicar num gráfico filtra a tela inteira na hora, sem recarregar a página."""
    template_name = 'dashboard_pro.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        questions = (
            Question.objects.filter(is_active=True, is_system=False)
            .prefetch_related('options')
            .order_by('order', 'id')
        )
        context['export_questions'] = [
            {
                'id': q.id,
                'key': q.key,
                'label': q.label,
                'category': q.category or 'Outras perguntas',
                'type': q.question_type,
                'options': [
                    {'label': o.label, 'value': o.effective_value, 'status': o.status}
                    for o in q.options.all()
                ],
            }
            for q in questions
        ]

        responses = PesquisaGravatai.objects.filter(is_duplicate=False).order_by('created_at')
        context['export_responses'] = list(responses.values('id', 'nome', 'whatsapp', 'created_at'))

        response_ids = [r['id'] for r in context['export_responses']]
        context['export_answers'] = list(
            Answer.objects.filter(response_id__in=response_ids, question__in=questions)
            .exclude(value='')
            .values_list('response_id', 'question_id', 'value')
        )

        context['total_duplicatas'] = PesquisaGravatai.objects.filter(is_duplicate=True).count()
        return context
