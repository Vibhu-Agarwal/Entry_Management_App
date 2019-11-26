from users.serializers import UserSerializer
from rest_framework import serializers
from django.conf import settings
from visit.models import Visit
from users.models import User
from management.mailing import send_host_email, send_visitor_checkout_email


class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = Visit
        fields = '__all__'

    def save(self, **kwargs):
        check_in_mail = False
        if self.instance is None:
            check_in_mail = True

        visit_instance = super(VisitSerializer, self).save(**kwargs)

        if settings.ALLOW_EMAILS:
            if check_in_mail:
                send_host_email(visit_instance)
            else:
                send_visitor_checkout_email(visit_instance)

        return visit_instance


class GETVisitSerializer(VisitSerializer):

    visitor = UserSerializer(read_only=True)
    host = UserSerializer(read_only=True)


class GETHostVisitSerializer(serializers.ModelSerializer):

    visitor = UserSerializer(read_only=True)

    class Meta:
        model = Visit
        exclude = ('host',)


class VisitorVisitSerializer(VisitSerializer):

    class Meta:
        model = Visit
        exclude = ('visitor',)


class CreateHostVisitSerializer(VisitorVisitSerializer):

    class Meta:
        model = Visit
        exclude = ('visitor', 'out_time')


class UpdateVisitorVisitSerializer(VisitorVisitSerializer):

    class Meta:
        model = Visit
        fields = ()


class GETVisitorVisitSerializer(VisitorVisitSerializer):

    host = UserSerializer(read_only=True)


class VisitAndVisitorSerializer(VisitSerializer):

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
