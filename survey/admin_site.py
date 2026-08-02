from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group, User


class VirtuAdminSite(admin.AdminSite):
    site_header = 'Pesquisas Virtu'
    site_title = 'Pesquisas Virtu'
    index_title = 'Painel administrativo'

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        if not request.user.is_superuser:
            # Esconde "Autenticação e Autorização" (Users/Groups) de quem não é
            # superusuário — jargão técnico que não interessa pro uso do dia a dia.
            app_list = [app for app in app_list if app['app_label'] != 'auth']
        return app_list


virtu_admin_site = VirtuAdminSite(name='admin')
virtu_admin_site.register(User, UserAdmin)
virtu_admin_site.register(Group, GroupAdmin)
