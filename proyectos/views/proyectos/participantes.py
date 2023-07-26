#rest_framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
#django
from django.shortcuts import get_object_or_404
from django.http import Http404 
#proyectos
from proyectos.serializers.lista_inscritos import ListaInscritoSerializer
from proyectos.models import Inscrito, Proyecto

class ProyectoParticpantesViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = ListaInscritoSerializer

    @action(detail=False, methods=['get'])
    def get_participantes(self, request, *args, **kwargs):
        """
        Obtiene la lista de participantes de un proyecto específico.

        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            *args: Argumentos adicionales.
            **kwargs: Argumentos de palabras clave adicionales.

        Returns:
            Response: Una respuesta HTTP con los datos de los participantes del proyecto.

        Raises:
            Http404: Si no se encuentra el proyecto o el inscrito correspondiente.
        """
        try:
            proyecto_id = kwargs['proyecto_id']

            proyecto = get_object_or_404(Proyecto, id=proyecto_id)

            inscrito = get_object_or_404(Inscrito, id=proyecto.aprendiz.id)

            inscritos = Inscrito.objects.filter(nombre_grupo_id=inscrito.nombre_grupo_id)

            serializer = self.get_serializer(inscritos, many=True)
            return Response(serializer.data)
        except Http404:
            return Response("Proyecto o inscrito no encontrado.", status=status.HTTP_404_NOT_FOUND)
