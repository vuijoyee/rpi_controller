# -*- coding: utf-8 -*-

from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify

# External Models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete

from rest_framework.authtoken.models import Token
from itsdangerous import JSONWebSignatureSerializer as Serializer

from rpi_controller.settings import SECRET_KEY

# Logger
import logging

logger = logging.getLogger('api_v1')


class Device(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    mac_address = models.CharField(null=False, max_length=128, default="0xFFFFFF")
    location = models.CharField(max_length=64)
    address = models.TextField(max_length=100, null=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=100, unique=True)

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('name', '') + "-" + str(timezone.now().strftime("LI%s")))
        super().__init__(*args, **kwargs)
        self.device_token = self._unique_device_id()

    def _generate_token(self):
        DeviceToken.objects.create(device_id=self.id)

    def _unique_device_id(self):
        s = Serializer(SECRET_KEY)
        token = s.dumps({'id': self.id}).decode('ascii')
        return token

    @staticmethod
    def verify_device_id(device_id):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(device_id)
        except:
            return None
        return Device.objects.get(id=data['id'])

    def __str__(self):
        return self.name


class Error(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=100)

    @staticmethod
    def failures_of_company(user):
        devices = Device.objects.filter(user=user)
        return Device.failures_of_lifts(devices)

    @staticmethod
    def failures_of_lifts(lifts):
        lst = []
        for lift in lifts:
            for error in Error.objects.all():
                if error.device == lift:
                    lst.append(error)
        return lst

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            kwargs['slug'] = slugify(kwargs.get('title', '') + "-" + str(timezone.now().strftime("FA%s")))
        super().__init__(*args, **kwargs)

    def __str__(self):
        return "Lift: %s | Title: %s | Date: %s" % (self.lift, self.title, self.created_at)


class Warning(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=100)
    api_url = models.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            slug = slugify(kwargs.get('title', '') + "-" + str(timezone.now().strftime("MM%s")))
            kwargs['slug'] = slug
        super().__init__(*args, **kwargs)

    @staticmethod
    def messages_of_company(user):
        lifts = Device.objects.filter(user=user)
        return Message.messages_of_lifts(lifts)

    @staticmethod
    def messages_of_lifts(lifts):
        lst = []
        for lift in lifts:
            for message in Message.objects.all():
                if message.lift == lift:
                    lst.append(message)
        return lst

    def __str__(self):
        return self.title


class Relay(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)

    A0 = models.BooleanField(default=False)
    A1 = models.BooleanField(default=False)
    A2 = models.BooleanField(default=False)
    A3 = models.BooleanField(default=False)
    A4 = models.BooleanField(default=False)
    A5 = models.BooleanField(default=False)
    A6 = models.BooleanField(default=False)
    A7 = models.BooleanField(default=False)

    def get_all(self):
        lst = {
            'A': {'A0': int(self.A0),
                  'A1': int(self.A1),
                  'A2': int(self.A2),
                  'A3': int(self.A3),
                  'A4': int(self.A4),
                  'A5': int(self.A5)},
        }
        return lst

    def __str__(self):
        return str(self.id)


class DigitalInput(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)

    DIN1 = models.BooleanField(default=False)
    DIN2 = models.BooleanField(default=False)
    DIN3 = models.BooleanField(default=False)
    DIN4 = models.BooleanField(default=False)

    def __str__(self):
        return str({'DIN1': self.DIN1,
                    'DIN2': self.DIN2,
                    'DIN3': self.DIN3,
                    'DIN4': self.DIN4})


class DigitalOutput(models.Model):
    device = models.OneToOneField(Device,on_delete=models.CASCADE)

    DOUT1 = models.BooleanField(default=False)
    DOUT2 = models.BooleanField(default=False)
    DOUT3 = models.BooleanField(default=False)
    DOUT4 = models.BooleanField(default=False)

    def __str__(self):
        return str({'DIN1': self.DOUT1,
                    'DIN2': self.DOUT2,
                    'DIN3': self.DOUT3,
                    'DIN4': self.DOUT4})


class AnalogInput(models.Model):
    device = models.OneToOneField(Device)

    AIN1 = models.IntegerField(default=0)
    AIN2 = models.IntegerField(default=0)

    def __str__(self):
        return str({'AIN1': self.AIN1,
                    'AIN2': self.AIN2})


class AnalogOutput(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)

    AOUT1 = models.IntegerField(default=0)
    AOUT2 = models.IntegerField(default=0)

    def __str__(self):
        return str({'AOUT1': self.AOUT1,
                    'AOUT2': self.AOUT2})


class Status(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    enable_control = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    slug = models.CharField(max_length=100)

    @property
    def is_in_monitor_mode(self):
        return not self.enable_control

    @property
    def is_in_controller_mode(self):
        return self.enable_control

    def get_pin_status(self):
        return self.pin_schema.get_all()

    def __init__(self, *args, **kwargs):
        if not 'slug' in kwargs:
            slug = slugify(kwargs.get('name', '') + "-" + str(timezone.now().strftime("ST%s")))
            kwargs['slug'] = slug
        super().__init__(*args, **kwargs)

    def __str__(self):
        return self.name


class DeviceToken(models.Model):
    device = models.OneToOneField(Device, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    token = models.CharField(max_length=256)
    serializer = Serializer(SECRET_KEY)

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            data = s.loads(token)
        except:
            logger.debug('Exception on Verifying Token')
            return None
        return Device.objects.get(id=data['device_id'])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            token = self.serializer.dumps({'device_id': kwargs['device'].id}).decode('ascii')
            self.token = token
        except KeyError:
            pass


def create_device_related_models(sender, instance=None, created=False, **kwargs):
    if created:
        Relay.objects.create(device=instance)
        AnalogInput.objects.create(device=instance)
        AnalogOutput.objects.create(device=instance)
        DigitalInput.objects.create(device=instance)
        DigitalOutput.objects.create(device=instance)
        Error.objects.create(device=instance)
        Warning.objects.create(device=instance)
        Status.objects.create(device=instance)
        DeviceToken.objects.create(device=instance)

post_save.connect(create_device_related_models, sender=Device)