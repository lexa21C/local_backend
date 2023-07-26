from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from proyectos.serializers.proyecto import ProyectoSerializer
from proyectos.models import Inscrito, Proyecto
from proyectos.views.funciones import *
from django.http import Http404

from rest_framework.exceptions import NotFound

class ProyectosAprendizViewSet(viewsets.ModelViewSet):
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_proyectos_aprendiz(self, request, *args, **kwargs):
        """
        Obtiene los proyectos asociados a un usuario específico.

        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            *args: Argumentos adicionales.
            **kwargs: Argumentos de palabras clave adicionales.

        Returns:
            Response: Una respuesta HTTP con los datos de los proyectos asociados al usuario.
        """
        try:
            user_id = kwargs['user_id']
            perfil_id = perfil_conectado(user_id)
            inscrito = Inscrito.objects.filter(perfil_id=perfil_id)
            grupo_ids = inscrito.values_list('nombre_grupo', flat=True)
            inscritos = Inscrito.objects.filter(nombre_grupo__id__in=grupo_ids)
            integrante_ids = inscritos.values_list('id', flat=True)
            proyectos = Proyecto.objects.filter(aprendiz__id__in=integrante_ids)
            
            if not proyectos.exists():
                raise NotFound("No se encontraron proyectos para este perfil.")
            
            serializer = self.get_serializer(proyectos, many=True)
            return Response(serializer.data)
        except Http404:
            return Response("Perfil no encontrado.", status=status.HTTP_404_NOT_FOUND)
