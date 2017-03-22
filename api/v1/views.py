
import json
import logging

from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from api.v1.serializers import *
from api.v1.models import *

logger = logging.getLogger('api')


@api_view(['GET', 'POST'])
def lift_controller(request, pk):
    if request.user.is_anonymous:
        print(request.POST)
        if 'auth-token' in request.POST:
            print(request.POST)
            device = Device.verify_device_id(request.POST['auth-token'])
            if device:
                serializer = DeviceSerializer(device)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'message': "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        else:
            return Response({'message': "Unauthorized Request",
                             'status_code': 401}, status=status.HTTP_401_UNAUTHORIZED)

    else:
        try:
            device = Device.objects.get(pk=pk)
        except Device.DoesNotExist:
            return HttpResponse(status=404)
        return Response({'device': device.name,
                         'is_control_enabled': device.enable_control,
                         'pin_diagram': device.relay.get_all()})


@api_view(['POST'])
def get_auth_token(request):
    if request.method == "POST":
        try:
            print(json.loads(request.body.decode('utf-8')))
        except:
            print(">>> JSON failed")
            pass
        print(request.META['CONTENT_TYPE'])
        print(request.POST)
        if 'mac-address' and 'passcode' in request.POST:
            try:
                device = Device.objects.get(mac_address=request.POST['mac-address'])
                token = DeviceToken.objects.get(device_id=device.id).token
                content = {
                    'lift-id': device.id,
                    'lift-slug': device.slug,
                    'lift-token': token
                }
                return Response(content, status=status.HTTP_200_OK)

            except Device.DoesNotExist:
                return Response({'detail': 'lift not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'detail': 'please send your identity'}, status=status.HTTP_401_UNAUTHORIZED)
            # TODO: ELSE??


@api_view(['GET', 'POST'])
def device_hub(request):
    try:
        print(json.loads(request.body.decode('utf-8')))
    except:
        print(">>> JSON failed")
        pass
    print(request.META['CONTENT_TYPE'])
    print(request.POST)
    if request.method == "POST" and \
            "mac-address" and "lift-token" in request.POST:
        try:
            device = Device.objects.get(mac_address=request.POST['mac-address'])
            device_test = DeviceToken.objects.get(token=request.POST['lift-token'])
            if device_test:
                if device.id == device_test.id:
                    serializer = DeviceSerializer(device, context={'request': request})
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {'detail': 'token authentication failed. token does not match with your mac address'},
                        status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'detail': 'token authentication failed. token does not match with your mac address'},
                                status=status.HTTP_401_UNAUTHORIZED)

        # TODO implement LiftToken.DoesNotExist exception for less and clean code
        # TODO e.g except Lift.DoesNotExist or LiftToken.DoesNotExist
        except DeviceToken.DoesNotExist or DeviceToken.DoesNotExist:
            return Response({'detail': 'identity check failed'}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        if "mac_address" and "lift-token" in request.GET:
            return Response({'detail': 'Method <GET> not allowed'})

    else:
        return Response({'detail': 'identity check failed'}, status=status.HTTP_403_FORBIDDEN)


class UserList(APIView):
    def get(self, request):
        if request.user.is_superuser:
            users = User.objects.all()
            serializer = UserSerializer(users, many=True, context={'request': request})
            return Response(serializer.data)
        else:
            return Response({'detail': 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)


class UserDetail(APIView):
    def get(self, request, username):
        user = get_object_or_404(User, username=username)
        if not user == request.user:
            return Response({'detail': 'unauthorized request'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)


# -------------------------------------  Device Model View ------------------------------- #
class DeviceList(APIView):
    """
    List devices of current user.
    """

    def get(self, request, format=None):
        devices = Device.objects.filter(user_profile=request.user)
        serializer = DeviceSerializer(devices, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    # TODO Create Device with this View
    def post(self, request, format=None):
        if request.user:
            serializer = DeviceSerializer(relays, data=request.data)

            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeviceDetail(APIView):
    """
    Detailed Lift View
    """

    def get(self, request, pk, format=None):
        device = get_object_or_404(Device, pk=pk)
        serializer = DeviceSerializer(device, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        pass


# --------------------------------------------------------------------------------------- #

class StatusDetail(APIView):
    """
    Status Detail of Lift Object
    """

    def get(self, request, pk, format=None):
        status = Status.objects.filter(lift_id=pk)
        serializer = StatusSerializer(status, context={'request': request})
        return Response(serializer.data)


class RelayDetail(APIView):
    """
    Pin Detail View
    """

    # permission_classes = (IsAuthenticated,)
    # TODO Only Return the Pin Status that belongs to Lift

    def get(self, request, pk, format=None):
        lift = get_object_or_404(Device, pk=pk)
        device = lift.status.pin_schema
        serializer = DeviceSerializer(device, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        device = get_object_or_404(Device, pk=pk)
        relay = device.relay
        serializer = RelaySerializer(relay, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalogInputDetail(APIView):
    def get(self, request, pk, format=None):
        lift = get_object_or_404(Lift, pk=pk)
        analog_input = lift.analoginput
        serializer = AnalogInputSerializer(analog_input, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        # TODO: Ensure the route only accessable from raspberry pi
        print(request.data)
        lift = get_object_or_404(Lift, pk=pk)
        analog_input = lift.analoginput
        serializer = AnalogInputSerializer(analog_input, data=request.data)
        if request.data:
            if not "lift" in request.data:
                request.data["lift"] = lift.pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnalogOutputDetail(APIView):
    def get(self, request, pk, format=None):
        lift = get_object_or_404(Lift, pk=pk)
        analog_output = lift.analogoutput
        serializer = AnalogOutputSerializer(analog_output, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        lift = get_object_or_404(Lift, pk=pk)
        analog_output = lift.analogoutput
        serializer = AnalogOutputSerializer(analog_output, data=request.data)
        if request.data:
            if not "lift" in request.data:
                request.data["lift"] = lift.pk
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DigitalInputDetail(APIView):
    def get(self, request, pk, format=None):
        print(request.user)
        lift = get_object_or_404(Device, pk=pk)
        digital_input = lift.digitalinput
        serializer = DigitalInputSerializer(digital_input, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, format=None):
        # TODO: Ensure the route only accessable from raspberry pi
        device = get_object_or_404(Device, pk=pk)
        digital_input = device.digitalinput
        serializer = DigitalInputSerializer(digital_input, data=request.data)
        if request.data:
            if not "device" in request.data:
                request.data["device"] = device.pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DigitalOutputDetail(APIView):
    def get(self, request, pk, format=None):
        device = get_object_or_404(Device, pk=pk)
        digital_output = device.digitaloutput
        serializer = DigitalOutputSerializer(digital_output, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        device = get_object_or_404(Device, pk=pk)
        digital_output = device.digitaloutput
        serializer = DigitalOutputSerializer(digital_output, data=request.data)
        if request.data:
            if not "device" in request.data:
                request.data["device"] = lift.pk
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)