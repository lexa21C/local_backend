#django
from django.shortcuts import get_object_or_404
from django.http import Http404  # Importar la excepción Http404
#rest_framework
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
#proyecto
from proyectos.serializers.lista_inscritos import ListaInscritoSerializer
from proyectos.models import Inscrito , Ficha

class FichaIntegrantesViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = ListaInscritoSerializer
    # permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['get'])
    def get_ficha_inscritos(self, request, *args, **kwargs):
        """
        Obtiene los inscritos asociados a una ficha específica.

        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            *args: Argumentos adicionales.
            **kwargs: Argumentos de palabras clave adicionales.

        Returns:
            Response: Una respuesta HTTP con los datos de los inscritos asociados a la ficha.

        Raises:
            Http404: Si la ficha no existe.
        """
        try:
            ficha_id = kwargs['ficha_id']
            ficha = get_object_or_404(Ficha, id=ficha_id)

            inscritos = Inscrito.objects.filter(ficha=ficha)
            #serializar el perfil con un depth 2
            serializer = self.get_serializer(inscritos, many=True)
            return Response(serializer.data)
        except Http404:
            return Response("Ficha no encontrada.", status=status.HTTP_404_NOT_FOUND)
