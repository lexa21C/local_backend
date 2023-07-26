from rest_framework import serializers
from proyectos.models import Entrega

class EntregaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Entrega
        fields = ['id','calificacion' ,'descripcion_entrega','documento','respuesta_instructor','instructor','proyecto', 'tipo_revision','autor','creado', 'editado']
