from rest_framework import serializers
from proyectos.models import Ficha

class FichaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ficha
        fields = ['url','id', 'codigo', 'fecha_inicio', 'fecha_finalizacion','modalidad','programa']

