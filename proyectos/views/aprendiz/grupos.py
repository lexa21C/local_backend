#django
from django.http import Http404 
from django.shortcuts import get_object_or_404
#rest_framework
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
#proyectos
from proyectos.serializers.lista_inscritos import *
from proyectos.views.funciones import *

class UsuarioGruposViewSet(viewsets.ModelViewSet):
    queryset = Inscrito.objects.all()
    serializer_class = ListaInscritoSerializer
    # permission_classes = [permissions.IsAuthenticated]
    def get_mis_grupos(self, request, *args, **kwargs):
        """
        Obtiene la lista de grupos a los que pertenece un usuario específico.

        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            *args: Argumentos adicionales.
            **kwargs: Argumentos de palabras clave adicionales.

        Returns:
            Response: Una respuesta HTTP con los datos de los grupos a los que pertenece el usuario, o un mensaje de error si el usuario no existe.

        Raises:
            User.DoesNotExist: Si el usuario especificado no existe.
        """
        try:
            user_id = kwargs['user_id']
            perfil_id = perfil_conectado(user_id)
            inscritos = Inscrito.objects.filter(perfil_id=perfil_id, nombre_grupo__isnull=False)
            
            if inscritos.exists():
                # Serializar los datos de los inscritos
                serializer = self.get_serializer(inscritos, many=True)
                return Response(serializer.data)
            else:
                return Response("El usuario no tiene ningún grupo asociado.", status=status.HTTP_404_NOT_FOUND)
        except Http404:
            return Response("Perfil no encontrado.", status=status.HTTP_404_NOT_FOUND)

