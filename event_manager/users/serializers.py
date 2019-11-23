from users.models import User, OfficeBranch
from users.helpers import make_password
from rest_framework import serializers


class OfficeBranchSerializer(serializers.ModelSerializer):

    class Meta:
        model = OfficeBranch
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):

    office_branch = OfficeBranchSerializer

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'avatar', 'email', 'phone_number', 'office_branch')


class HostCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone_number', 'office_branch')

    def create(self, validated_data):
        host = super(HostCreateSerializer, self).create(validated_data)
        host.set_password(make_password())
        host.save()
        return host


class VisitorCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar', 'email', 'phone_number')
