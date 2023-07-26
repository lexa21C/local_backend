
#Django
from django.contrib.auth import  authenticate
from django.contrib.auth.password_validation import validate_password

#django REST Framework
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from proyectos.models import Perfil

class UserSignUpSerializer(serializers.Serializer):
    #User login serializer
    #Handle the  login request data
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]

    )
    #Password
    password = serializers.CharField(min_length=8,max_length=64)
    password_confirmation = serializers.CharField(min_length=8,max_length=64)

    #name
    first_name = serializers.CharField(min_length=2, max_length=30)
    last_name = serializers.CharField(min_length=2, max_length=30)

    # def validate(self, data):
    #     #verificar contraseñas
    #     passwd = data['password']
    #     passwd_conf = data['password_confirmation']
    #     if passwd != passwd_conf:
    #         raise serializers.ValidationError('contraseñas no coinciden')
    #     password_validation.validate.password(passwd)
    #     return data
    def validate(self, data):
        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError('contraseñas no coinciden')
        validate_password(passwd)
        return data


    # def create(self, data):
    #     data.pop('password_confirmation')
    #     user = User.objects.create_user(**data)
    #     perfil = Perfil.objects.create(user=user)
    #     return user
    def create(self, validated_data):
        password = validated_data.pop('password')
        password_confirmation = validated_data.pop('password_confirmation')
        if password != password_confirmation:
            raise serializers.ValidationError('Las contraseñas no coinciden')
        user = User.objects.create_user(**validated_data, password=password)
        #perfil = Perfil.objects.create(User=user)  # Aquí pasa el objeto "user" al crear el objeto "Perfil"
        return user


