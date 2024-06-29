from rest_framework import serializers
from api.models import VirtualMachine

class VirtualMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMachine
        fields = '__all__'