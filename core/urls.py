from django.urls import path, include

from survey.admin_site import virtu_admin_site

urlpatterns = [
    path('admin/', virtu_admin_site.urls),
    path('', include('survey.urls')),
]