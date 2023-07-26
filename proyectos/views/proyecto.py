from rest_framework import viewsets
from rest_framework import permissions
from proyectos.serializers.proyecto import *
from rest_framework import status
from rest_framework.response import Response

class ProyectoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Proyecto.objects.all()
    serializer_class = ProyectoSerializer
 

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        proyecto = serializer.save()
        return Response(ProyectoSerializer(proyecto, context={'request': request}).data, status=status.HTTP_201_CREATED)
