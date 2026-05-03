from django.urls import path
# ATENÇÃO AQUI: Garanta que o DashboardView está sendo importado junto com as outras!
from .views import SurveyView, SuccessView, DashboardView

urlpatterns = [
    path('', SurveyView.as_view(), name='survey_home'),
    path('obrigado/', SuccessView.as_view(), name='survey_success'),
    # A rota do painel que adicionamos
    path('painel/', DashboardView.as_view(), name='dashboard'),
]