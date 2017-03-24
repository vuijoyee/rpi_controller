from django.contrib.auth.models import User
from django.shortcuts import reverse

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
    lifts = serializers.SerializerMethodField('_get_lifts')

    class Meta:
        model = User
        fields = ('url', 'email', 'username', 'lifts', 'password', 'last_login', 'date_joined')
        extra_kwargs = {'password': {'write_only': True}}

    def _get_lifts(self, obj):
        lifts = Device.objects.filter(user=obj.user)
        return [{'id': x.id, 'name': x.name} for x in lifts]

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
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
    OUT1 = serializers.IntegerField(required=True)
    OUT2 = serializers.IntegerField(required=True)

    class Meta:
        model = AnalogOutput
        exclude = ('id', 'device',)


class DigitalInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalInput
        exclude = ('id', 'device',)


class DigitalOutputSerializer(serializers.ModelSerializer):
    OUT1 = serializers.BooleanField(required=True)
    OUT2 = serializers.BooleanField(required=True)

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

    class Meta:
        model = Device
        fields = ('url', 'id', 'name', 'location', 'address', 'created_at', 'slug')


class ErrorSerializer(serializers.ModelSerializer):
    device = serializers.HyperlinkedRelatedField(view_name="api.device.detail",
                                                 lookup_field="pk",
                                                 many=False,
                                                 read_only=True)

    class Meta:
        model = Error
        fields = ('device', 'title', 'content', 'created_at', 'is_solved', 'slug')
