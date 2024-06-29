from django.shortcuts import render

from rest_framework import generics
from .models import *
from .serializers import *

class VirtualMachine(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer

# class VirtualMachineDetail(viewsets.ModelViewSet):
#     queryset = VirtualMachine.objects.all()
#     serializer_class = VirtualMachineSerializer

