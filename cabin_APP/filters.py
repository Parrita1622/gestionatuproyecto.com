import django_filters
from .models import Proyecto

class ProyectoFilter(django_filters.FilterSet):
    # Define un filtro personalizado para buscar por el ID de usuario
    username_id = django_filters.CharFilter(field_name='username__id', label='ID de Usuario')

    class Meta:
        model = Proyecto
        fields = ['nombre', 'superficie', 'fecha_inicio', 'username_id']  # Agrega otros campos de búsqueda aquí si es necesario
