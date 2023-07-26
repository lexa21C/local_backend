from rest_framework import serializers
from proyectos.models import Inscrito
# from proyectos.serializers.grupo import GrupoSerializer
# from proyectos.serializers.ficha import FichaSerializer

class InscritoSerializer(serializers.ModelSerializer):


    class Meta:
        model = Inscrito
        fields = ['id', 'estado','nombre_grupo', 'perfil', 'ficha']
        # depth = 2
