from django.views.generic import CreateView, TemplateView
from django.urls import reverse_lazy
from .models import PesquisaGravatai
from .forms import PesquisaForm
from .tasks import enviar_email_task

class SurveyView(CreateView):
    model = PesquisaGravatai
    form_class = PesquisaForm
    template_name = 'survey.html'
    success_url = reverse_lazy('survey_success')

    def form_valid(self, form):
        response = super().form_valid(form)
        # Dispara o Celery
        enviar_email_task.delay(form.cleaned_data)
        return response

class SuccessView(TemplateView):
    template_name = 'success.html'