from users.models import User
from users.helpers import make_password
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar', 'email', 'phone_number', 'user_type')


class HostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone_number')

    def create(self, validated_data):
        host = super(HostCreateSerializer, self).create(validated_data)
        host.set_password(make_password())
        host.save()
        return host


class VisitorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone_number')
