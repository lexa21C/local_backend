from rest_framework import serializers
from proyectos.models import Rol

class RolSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Rol
        fields = ['url', 'id','nombre']

