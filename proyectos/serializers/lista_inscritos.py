from rest_framework import serializers
from proyectos.models import Inscrito

class ListaInscritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inscrito
        fields = ['id','estado','perfil','nombre_grupo','ficha']
        depth = 2
        
    