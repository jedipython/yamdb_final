from .models import User

from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        fields = ('first_name', 'last_name',
                  'username', 'bio', 'email', 'role',)
        model = User
