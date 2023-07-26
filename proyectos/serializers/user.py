from django.contrib.auth.models import User
from rest_framework import serializers


class UserModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields =('id', 'username', 'first_name', 'last_name', 'email',)

        
    
    # def create(self, validated_data):
    #     user = User.objects.create(
    #         username=validated_data['username'],
    #         email=validated_data['email'],
    #     )
    #     user.set_password(validated_data['password'])
    #     user.save()
    #     return user
