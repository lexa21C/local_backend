#Users views

# Django REST FRAMEWORK
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from proyectos.models import Perfil
#serializer
from proyectos.serializers.login import *
from proyectos.serializers.user import *
from proyectos.serializers.perfil import PerfilSerializer

class UserLoginAPIView(APIView):

    
    def post(self, request, *args, **kwargs):
        
        #Hadlle HTTP POST    request.
        serializer =  UserLoginSerializer(data=request.data)

        print("xxxxxxxxxxxxxxxxx")
        print(serializer)
        print("xxxxxxxxxxxxxxxxx")
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        p=Perfil.objects.get(usuario = user)
        data = {
            'user': UserModelSerializer(user).data,
            'access_token': token,
            # 'otro': PerfilSerializer().data
            'otro': p.rol.nombre
        }
        return Response(data, status=status.HTTP_201_CREATED)
