from rest_framework import serializers
from proyectos.models import Proyecto

class ListaProyectoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Proyecto
        fields = ['id', 'nombre_proyecto', 'descripcion', 'aprendiz', 'codigo_fuente', 'categorias', 'estado', 'calificacion']
        depth = 2
