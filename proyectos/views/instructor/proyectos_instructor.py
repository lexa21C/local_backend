#rest_framework
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
#django
from django.http import Http404 
from django.shortcuts import get_object_or_404
#proyectos
from proyectos.models import Inscrito, Proyecto, Entrega, Ficha
from proyectos.serializers.lista_proyectos import ListaProyectoSerializer

class ProyectosInstructorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Proyecto.objects.all()
    serializer_class = ListaProyectoSerializer

    @action(detail=True, methods=['get'])
    def get_proyectos_instructor(self, request, *args, **kwargs):
        """
        Obtiene los proyectos asociados a una ficha específica y actualiza el atributo "calificacion" de los proyectos según su estado y las entregas asociadas.

        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            *args: Argumentos adicionales.
            **kwargs: Argumentos de palabras clave adicionales.

        Returns:
            Response: Una respuesta HTTP con los datos de los proyectos actualizados.

        Raises:
            Http404: Si la ficha no existe.
        """
        try:
            ficha_id = kwargs['ficha_id']
            ficha = get_object_or_404(Ficha, id=ficha_id)

            inscritos = Inscrito.objects.filter(ficha=ficha)
            integrante_ids = inscritos.values_list('id', flat=True)

            proyectos = Proyecto.objects.filter(aprendiz__id__in=integrante_ids)

            # Cambiar el estado del atributo "calificacion" de los proyectos
            for proyecto in proyectos:
                # Realiza las condiciones y cambios necesarios en el atributo "calificacion"
                if proyecto.estado == 'terminado' or proyecto.estado == 'en desarrollo':
                    entregas = Entrega.objects.filter(proyecto=proyecto.id)

                    # Verificar si todas las entregas tienen la misma calificación
                    calificaciones = entregas.values_list('calificacion', flat=True).distinct()
                    if len(calificaciones) == 1:
                        calificacion = calificaciones[0]
                        if calificacion == 'aprobado':
                            proyecto.calificacion = 'calificado'
                        elif calificacion == 'en revision':
                            proyecto.calificacion = 'calificar entrega'
                        elif calificacion == 'No aprobado':
                            proyecto.calificacion = 'entrega no aprobada'
                    else:
                        proyecto.calificacion = 'calificar entrega'
                elif proyecto.estado == 'anulado':
                    proyecto.calificacion = 'calificar entrega'
                else:
                    proyecto.calificacion = 'calificar proyecto'

                proyecto.save()  # Guardar los cambios en la base de datos

            serializer = self.get_serializer(proyectos, many=True)
            return Response(serializer.data)
        except Http404:
            return Response("Ficha no encontrada.", status=status.HTTP_404_NOT_FOUND)
