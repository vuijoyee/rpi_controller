from django.conf.urls import url
from api.v1.views import *

import logging

logger = logging.getLogger('api')

urlpatterns = [

    # User URLs
    url(r'^user/$', UserList.as_view(), name='user_list'),
    url(r'^user/(?P<username>[\w-]+)/$', UserDetail.as_view(), name='api.user.detail'),

    # Device URLs
    url(r'^devices/$', DeviceList.as_view(), name='api.lift_list'),
    url(r'^device/(?P<pk>[0-9]+)/$', DeviceDetail.as_view(), name='api.device.detail'),

    # Device Controlling URLs
    url(r'^device/(?P<pk>[0-9]+)/controller/$', lift_controller, name='api.lift.controller'),
    url(r'^device/(?P<pk>[0-9]+)/controller/enable/$', lift_controller_enable, name='api.device.control_enable'),
    url(r'^device/(?P<pk>[0-9]+)/controller/disable/$', lift_controller_disable, name='api.device.control_disable'),

    # Device Status URLs
    url(r'^device/(?P<pk>[0-9]+)/status/$', StatusDetail.as_view(), name='api.device.status'),
    url(r'^device/(?P<pk>[0-9]+)/relay/$', RelayDetail.as_view(), name='api.device.relay'),

    url(r'^device/(?P<pk>[0-9]+)/analog-input/$', AnalogInputDetail.as_view(), name='api.device.analog_input'),
    url(r'^device/(?P<pk>[0-9]+)/analog-output/$', AnalogOutputDetail.as_view(), name='api.device.analog_output'),

    url(r'^device/(?P<pk>[0-9]+)/digital-input/$', DigitalInputDetail.as_view(), name='api.device.digital_input'),
    url(r'^device/(?P<pk>[0-9]+)/digital-output/$', DigitalOutputDetail.as_view(), name='api.device.digital_output'),

    # Device Hub
    url(r'^device-hub/$', device_hub, name='api.device_hub'),
    url(r'^device-auth-token/$', get_auth_token, name='api.device_auth_token'),

]
