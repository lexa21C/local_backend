from rest_framework import serializers
from proyectos.models import Perfil
# from django.contrib.auth.models import User 

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perfil
        fields = [ 'url','id','documento', 'rol', 'usuario', 'tipo_documento', 'direccion', 'telefono', 'foto', 'web', 'creado', 'editado', ]
       



