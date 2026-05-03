from django.views.generic import CreateView, TemplateView, View, ListView
from django.views.generic import ListView # <- PRECISA TER ISSO NO TOPO
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

class DashboardView(ListView):
    model = PesquisaGravatai
    template_name = 'dashboard.html'
    context_object_name = 'pesquisas'
    ordering = ['-id'] # Traz os mais recentes primeiro

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Passamos também o total de respostas para criar um card de métrica
        context['total_respostas'] = PesquisaGravatai.objects.count()
        return context