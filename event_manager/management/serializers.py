from rest_framework import serializers
from management.models import ManagementTokenAuth


class ManagementTokenAuthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ManagementTokenAuth
        fields = "__all__"
