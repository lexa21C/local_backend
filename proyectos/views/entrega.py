from rest_framework import viewsets
from rest_framework import permissions
from proyectos.serializers.entrega import *

from rest_framework import status
from rest_framework.response import Response

class EntregaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Entrega.objects.all()
    serializer_class = EntregaSerializer
    # permission_classes = [permissions.IsAuthenticated]

    # get post delete update/put
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        entrega = serializer.save()
        return Response(EntregaSerializer(entrega, context={'request': request}).data, status=status.HTTP_201_CREATED)