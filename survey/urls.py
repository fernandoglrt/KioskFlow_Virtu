from django.urls import path
from .views import SurveyView, SuccessView

urlpatterns = [
    path('', SurveyView.as_view(), name='survey_home'),
    path('obrigado/', SuccessView.as_view(), name='survey_success'),
]