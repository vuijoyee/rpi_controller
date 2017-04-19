from django.contrib.auth.models import User

from rest_framework import serializers
from api.v1.models import (
    Device,
    Error,
    Warning,
    Status,
    Relay,
    AnalogInput,
    AnalogOutput,
    DigitalInput,
    DigitalOutput)

import logging

logger = logging.getLogger('api.v1.serializer')


class IndexSerializer:
    name = ""
    auth_url = ""
    lift_status_url = ""
    lift_control_url = ""

    def __init__(self):
        self.name = "Bor Remote Controller"
        self.lift_control_url = "/api/lift/<pk>/controller/"

    def data(self):
        return {'name': self.name,
                'auth_url': self.auth_url,
                'lift_control_url': self.lift_control_url}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='user_detail',
        lookup_field='username',
    )
    devices = serializers.SerializerMethodField('_get_devices')

    class Meta:
        model = User
        fields = ('url', 'email', 'username', 'lifts', 'password', 'last_login', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ('id',)

    def _get_devices(self, obj):
        devices = Device.objects.filter(user=obj.user)
        return [{'id': x.id, 'name': x.name} for x in devices]

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class RelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Relay
        exclude = ('id',)


class AnalogInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalogInput
        exclude = ('id', 'device',)


class AnalogOutputSerializer(serializers.ModelSerializer):
    AOUT1 = serializers.IntegerField(required=True)
    AOUT2 = serializers.IntegerField(required=True)

    class Meta:
        model = AnalogOutput
        exclude = ('id', 'device',)


class DigitalInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalInput
        exclude = ('id', 'device',)


class DigitalOutputSerializer(serializers.ModelSerializer):
    DOUT1 = serializers.BooleanField(required=True)
    DOUT2 = serializers.BooleanField(required=True)

    class Meta:
        model = DigitalOutput
        exclude = ('id', 'device',)


class StatusSerializer(serializers.ModelSerializer):
    relays = RelaySerializer(read_only=True)

    class Meta:
        model = Status


class DeviceSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='api.device.detail',
        lookup_field='pk'
    )
    id = serializers.ReadOnlyField()
    digitaloutput = DigitalOutputSerializer()
    digitalinput = DigitalInputSerializer()
    analogoutput = AnalogOutputSerializer()
    analoginput = AnalogInputSerializer()
    relay = RelaySerializer()

    class Meta:
        model = Device
        fields = ('url',
                  'id',
                  'name',
                  'location',
                  'address',
                  'created_at',
                  'slug',
                  'analogoutput',
                  'analoginput',
                  'digitaloutput',
                  'digitalinput',
                  'relay',)


class ErrorSerializer(serializers.ModelSerializer):
    device = serializers.HyperlinkedRelatedField(view_name="api.device.detail",
                                                 lookup_field="pk",
                                                 many=False,
                                                 read_only=True)

    class Meta:
        model = Error
        fields = ('device', 'title', 'content', 'created_at', 'is_solved', 'slug')
