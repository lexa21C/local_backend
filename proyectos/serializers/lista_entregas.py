from rest_framework import serializers
from proyectos.models import Entrega

class ListaEntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = ['id','calificacion', 'creado', 'editado' ,'descripcion_entrega','respuesta_instructor','instructor','proyecto', 'tipo_revision','autor']
        depth = 1