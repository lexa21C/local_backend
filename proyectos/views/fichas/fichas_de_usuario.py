#django
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User 
from django.http import Http404
#rest_framework
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
#proyecto
from proyectos.models import Inscrito, Ficha
from proyectos.serializers.lista_fichas import *
from proyectos.views.funciones import *


class FichasDeUsuarioViewSet(viewsets.ModelViewSet):
    """
    Punto de acceso de la API que permite ver o editar usuarios.
    """
    queryset = Ficha.objects.all()
    serializer_class = FichaSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_fichas(self, request, *args, **kwargs):
        """
        Obtiene las fichas asociadas al perfil conectado de un usuario.

        Args:
            request (HttpRequest): El objeto de solicitud HTTP.
            kwargs (dict): Argumentos de palabras clave extraídos de la URL.

        Returns:
            Response: Los datos serializados de las fichas obtenidas.

        Raises:
            Http404: Si no se encuentra el usuario, el perfil o la ficha (inscrito).
        """
        try:
            # Obtiene el ID del usuario de los argumentos de la URL
            user_id = kwargs['user_id']
            # Obtiene el ID del perfil conectado al usuario
            perfil_id = perfil_conectado(user_id)
            # Filtra las fichas (inscritos) por el perfil ID obtenido
             # Filtra los inscritos por el perfil ID obtenido y obtiene los valores de los IDs de las fichas
            inscrito = Inscrito.objects.filter(perfil_id=perfil_id)
            ficha_ids = inscrito.values_list('ficha', flat=True)
            fichas = Ficha.objects.filter(id__in=ficha_ids)
            # Serializa los objetos inscrito
            serializer = self.get_serializer(fichas, many=True)
            return Response(serializer.data)
        except (Http404, Inscrito.DoesNotExist):
            # Si el usuario, perfil o ficha (inscrito) no existe, lanza un error 404 con un mensaje adecuado
            raise Http404("Usuario, perfil o ficha no encontrados.")
