from users.serializers import UserSerializer
from rest_framework import serializers
from visit.models import Visit


class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = '__all__'


class GETVisitSerializer(VisitSerializer):

    visitor = UserSerializer(read_only=True)
    host = UserSerializer(read_only=True)


class GETHostVisitSerializer(serializers.ModelSerializer):

    visitor = UserSerializer(read_only=True)

    class Meta:
        model = Visit
        exclude = ('host',)


class GETVisitorVisitSerializer(serializers.ModelSerializer):

    host = UserSerializer(read_only=True)

    class Meta:
        model = Visit
        exclude = ('visitor',)
