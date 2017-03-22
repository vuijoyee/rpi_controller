from django.db.models.signals import post_save
from api.v1.models import *


def create_device_related_models(sender, instance=None, created=False, **kwargs):
    if created:
        Relay.objects.create(device=instance)
        print("Relay Model Created")

        AnalogInput.objects.create(device=instance)
        print("AnalogInput Model Created")

        AnalogOutput.objects.create(device=instance)
        print("AnalogOutput Model Created")

        DigitalInput.objects.create(device=instance)
        print("DigitalInput Model Created")

        DigitalOutput.objects.create(device=instance)
        print("DigitalOutput Model Created")

        Status.objects.create(pin_schema_id=pin.id, lift_id=instance.id)


post_save.connect(create_device_related_models, sender=Device)
