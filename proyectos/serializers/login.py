#Django
from django.contrib.auth import authenticate
#django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token

from proyectos.serializers.perfil import PerfilSerializer
from proyectos.serializers.user import UserModelSerializer


class UserLoginSerializer(serializers.Serializer):
    #User login serializer
    #Handle the  login request data
    #email = serializers.EmailField()
    username = serializers.CharField(min_length=4,max_length=20)
    password = serializers.CharField(min_length=8,max_length=64)

    def validate(self,  data):
        #verificar credenciales
        user = authenticate(username=data['username'], password=data['password'])
        #user = authenticate(username=data['email'],password=data['password'])
        #user = authenticate(request=request, email=email, password=password)
        
        print(user)
        if not user:
            raise serializers.ValidationError('invalido las credenciales')

        #limitar login a usurios con cuenta verificada
        # if not user.is_verified:
        #     raise serializer.ValidationError('cuenta no verificada')
        self.context['user']=user
        return data
    
    def create (self,data):
        #Genetate or retrieve new token
        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key









    # def create(self, data):
    # # Generate or retrieve new token
    #     token, created = Token.objects.get_or_create(user=self.context['user'])
    # # Serialize the user and token data
    #     user_data = UserModelSerializer(self.context['user']).data
    #     token_data = {'token': token.key}
    # # Serialize the user's profile data
    #     perfil_data = PerfilSerializer(self.context['user'].perfil).data
    # # Combine all the serialized data into a single dictionary
    #     return {**user_data, **token_data, **perfil_data}


        
        

# class UserLoginSerializer(serializers.Serializer):
#     #User login serializer
#     #Handle the  login request data
#     email = serializers.EmailField()
#     password = serializers.CharField(min_length=8,max_length=64)

#     def validate(self, data):
#         #verificar credenciales
#         user = authenticate(username=data['email'],password=data['password'])
#         print(user)
#         if not user:
#             raise serializers.ValidationError('invalido las credenciales')
#         self.context['user']=user
#         return data
    
#     def create (self,data):
#         #Genetate or retrieve new token
#         token, created = Token.objects.get_or_create(user=self.context['user'])
#         return self.context['user'], token.key
