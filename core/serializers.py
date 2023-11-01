from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer,UserSerializer as  BaseUserSerializer

from rest_framework import serializers

class UserCreateSerializer(BaseUserCreateSerializer):
    # birth_date = serializers.DateField()
    class Meta(BaseUserCreateSerializer.Meta):
        # fields = ['id','username','password','email','first_name','last_name','birth_date']
        fields = ['id','username','password','email','first_name','last_name'] 
 
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','email','username','first_name','last_name']