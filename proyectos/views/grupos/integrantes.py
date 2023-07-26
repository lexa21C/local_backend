from rest_framework import viewsets
from rest_framework import permissions
from proyectos.serializers.lista_inscritos import ListaInscritoSerializer
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from proyectos.views.funciones import perfil_conectado
from django.http import Http404  # Importar la excepción Http404
from proyectos.models import Inscrito, Grupo

class IntegrantesViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Inscrito.objects.all()
    serializer_class = ListaInscritoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_integrantes(self, request, *args, **kwargs):
        """
        Obtiene los inscritos asociados a un grupo específico.

        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            *args: Argumentos adicionales.
            **kwargs: Argumentos de palabras clave adicionales.

        Returns:
            Response: Una respuesta HTTP con los datos de los inscritos asociados al grupo.

        Raises:
            Http404: Si el grupo no existe.
        """
        try:
            grupo_id = kwargs['grupo_id']
            grupo = get_object_or_404(Grupo, id=grupo_id)

            inscritos = Inscrito.objects.filter(nombre_grupo=grupo)
            serializer = self.get_serializer(inscritos, many=True)
            return Response(serializer.data)
        except Http404:
            return Response("Grupo no encontrado.", status=status.HTTP_404_NOT_FOUND)

