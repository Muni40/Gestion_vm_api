from rest_framework import serializers
from .models import CPU, Memory, Disk, NetworkInterface, OperatingSystem, VirtualMachine, UsageHistory

class CPUSerializer(serializers.ModelSerializer):
    class Meta:
        model = CPU
        fields = '__all__'

class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'

class DiskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disk
        fields = '__all__'

class NetworkInterfaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NetworkInterface
        fields = '__all__'

class OperatingSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperatingSystem
        fields = '__all__'

class VirtualMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = VirtualMachine
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = str(instance.user)
        data['cpu'] = str(instance.cpu)
        data['memory'] = str(instance.memory)
        data['disk'] = str(instance.disk)
        data['network_interfaces'] = str(instance.network_interfaces)
        data['os'] = str(instance.os)
        return data

class UsageHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UsageHistory
        fields = '__all__'

class IPAddressSerializer(serializers.Serializer):
    ip_address = serializers.CharField()

    def validate_ip_address(self, value):\
        return value

class VirtualMachineIPSerializer(serializers.ModelSerializer):
    ip_addresses = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = VirtualMachine
        fields = ['id', 'ip_addresses']

    def update(self, instance, validated_data):
        ip_address = validated_data.get('ip_address')
        if ip_address:
            instance.add_ip_address(ip_address)
        return instance

    def remove_ip_address(self, instance, ip_address):
        instance.remove_ip_address(ip_address)
        return instance

    def add_ip_address(self, instance, ip_address):
        instance.add_ip_address(ip_address)
        return instance