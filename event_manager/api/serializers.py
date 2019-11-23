from users.models import User
from visit.models import Visit
from rest_framework import serializers


class VisitAndVisitorSerializer(serializers.ModelSerializer):

    class VisitorTempSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('first_name', 'last_name', 'avatar', 'email', 'phone_number')

    visitor = VisitorTempSerializer()

    class Meta:
        model = Visit
        exclude = ('out_time',)

    def create(self, validated_data):
        visitor_data = validated_data.pop('visitor')
        visitor = User.objects.create(**visitor_data)
        visit = Visit.objects.create(visitor=visitor, **validated_data)
        return visit
