from django.urls import path
from .views import SurveyView, SuccessView , SuccessView, DashboardView

urlpatterns = [
    path('', SurveyView.as_view(), name='survey_home'),
    path('obrigado/', SuccessView.as_view(), name='survey_success'),
    path('painel/', DashboardView.as_view(), name='dashboard'),

