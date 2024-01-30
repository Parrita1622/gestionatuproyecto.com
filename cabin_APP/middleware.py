from django.utils import timezone
from django.contrib.auth import logout
from .models import PlanUsuario 

class AutoDeactivateUsersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user

        if user.is_authenticated:
            current_time = timezone.now()
            one_month_ago = current_time - timezone.timedelta(days=33)
            three_months_ago = current_time - timezone.timedelta(days=93)
            one_year_ago = current_time - timezone.timedelta(days=368)
            admin_plan = current_time - timezone.timedelta(days=1828)

            try:
                plan_usuario = user.planusuario.plan_usuario
            except PlanUsuario.DoesNotExist:
                plan_usuario = None

            if user.date_joined <= one_month_ago and plan_usuario == 'Mensual':
                user.is_active = False
                user.save()
                logout(request)

            elif user.date_joined <= three_months_ago and plan_usuario == '3 Meses':
                user.is_active = False
                user.save()
                logout(request)

            elif user.date_joined <= one_year_ago and plan_usuario == 'Anual':
                user.is_active = False
                user.save()
                logout(request)
            
            elif user.date_joined <= admin_plan and plan_usuario == '5 años':
                user.is_active = False
                user.save()
                logout(request)

        response = self.get_response(request)
        return response

