#rest_framework
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
#django
from django.shortcuts import get_object_or_404
from django.http import Http404  # Importar la excepción Http404
#proyectos
from proyectos.serializers.lista_inscritos import *
from proyectos.views.funciones import *

class AgregarInscritosViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = ListaInscritoSerializer
    # permission_classes = [permissions.IsAuthenticated]
    
    def get_inscritos(self, request, *args, **kwargs):
        """
        Obtiene la lista de inscritos activos que no pertenecen a ningún grupo, están asociados
        a la misma ficha que un perfil específico y tienen el rol de 'aprendiz'.
        
        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            *args: Argumentos adicionales.
            **kwargs: Argumentos de palabras clave adicionales.

        Returns:
            Response: Una respuesta HTTP con los datos de los inscritos.

        Raises:
            Http404: Si no se encuentra el perfil correspondiente.
        """
        user_id = kwargs['id_user']
        perfil_id = perfil_conectado(user_id)
        inscritos = Inscrito.objects.filter(perfil_id=perfil_id, estado='activo', )
        
        # Obtener todas las fichas asociadas a los inscritos
        fichas = inscritos.values_list('ficha', flat=True).distinct()

        # Filtrar los inscritos que tienen alguna de las fichas asociadas
        # Filtrar los inscritos que tienen alguna de las fichas asociadas y cumplen las condiciones adicionales
        inscritos_misma_ficha = Inscrito.objects.filter(ficha__in=fichas, estado='activo', nombre_grupo__isnull=True )

        print( inscritos_misma_ficha)
        # Serializar los datos de los inscritos
        serializer = self.get_serializer(inscritos_misma_ficha, many=True)

        # Devolver la respuesta con los datos serializados
        return Response(serializer.data)