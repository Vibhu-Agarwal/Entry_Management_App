from rest_framework import serializers
from management.models import ManagementTokenAuth


class ManagementTokenAuthSerializer(serializers.ModelSerializer):
    """
    Serializer for 'ManagementTokenAuth' model to serialize its data
    """
    class Meta:
        model = ManagementTokenAuth
        fields = "__all__"
