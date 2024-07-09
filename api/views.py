from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import *
from .serializers import *

class IsOwnerOrReadOnly(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user

class CPUViewSet(viewsets.ModelViewSet):
    queryset = CPU.objects.all()
    serializer_class = CPUSerializer

class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer

class DiskViewSet(viewsets.ModelViewSet):
    queryset = Disk.objects.all()
    serializer_class = DiskSerializer

class NetworkInterfaceViewSet(viewsets.ModelViewSet):
    queryset = NetworkInterface.objects.all()
    serializer_class = NetworkInterfaceSerializer

class OperatingSystemViewSet(viewsets.ModelViewSet):
    queryset = OperatingSystem.objects.all()
    serializer_class = OperatingSystemSerializer

class UsageHistoryViewSet(viewsets.ModelViewSet):
    queryset = UsageHistory.objects.all()
    serializer_class = UsageHistorySerializer

class VirtualMachineViewSet(viewsets.ModelViewSet):
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer
    permission_classes = [IsOwnerOrReadOnly]

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        vm = self.get_object()
        vm.status = 'running'
        vm.save()
        return Response({'status': 'VM started'})

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        vm = self.get_object()
        vm.status = 'stopped'
        vm.save()
        return Response({'status': 'VM stopped'})

    @action(detail=True, methods=['get'])
    def monitor(self, request, pk=None):
        vm = self.get_object()
        data = {
            'cpu_usage': vm.cpu_usage,
            'memory_usage': vm.memory_usage,
            'disk_usage': vm.disk_usage,
            'status': vm.status,
        }
        return Response(data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        vm = self.get_object()
        stats_data = {
            'cpu_usage_history': self.get_cpu_usage_history(vm),
            'memory_usage_history': self.get_memory_usage_history(vm),
            'disk_usage_history': self.get_disk_usage_history(vm),
        }
        return Response(stats_data)
      
    @action(detail=True, methods=['get'])
    def usage_history(self, request, pk=None):
        vm = self.get_object()
        history = UsageHistory.objects.filter(vm=vm)
        serializer = UsageHistorySerializer(history, many=True)
        return Response(serializer.data)

    def get_cpu_usage_history(self, vm):
        history = UsageHistory.objects.filter(vm=vm).values_list('cpu_usage', flat=True)
        return list(history)

    def get_memory_usage_history(self, vm):
        history = UsageHistory.objects.filter(vm=vm).values_list('memory_usage', flat=True)
        return list(history)

    def get_disk_usage_history(self, vm):
        history = UsageHistory.objects.filter(vm=vm).values_list('disk_usage', flat=True)
        return list(history)

    @action(detail=True, methods=['post'])
    def assign_ip(self, request, pk=None):
        vm = self.get_object()
        serializer = IPAddressSerializer(data=request.data)
        if serializer.is_valid():
            ip_address = serializer.validated_data['ip_address']
            success, message = vm.assign_ip_address(ip_address)
            if success:
                return Response({'success': True, 'message': message})
            else:
                return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def remove_ip(self, request, pk=None):
        vm = self.get_object()
        serializer = IPAddressSerializer(data=request.data)
        if serializer.is_valid():
            ip_address = serializer.validated_data['ip_address']
            success, message = vm.remove_ip_address(ip_address)
            if success:
                return Response({'success': True, 'message': message})
            else:
                return Response({'success': False, 'message': message}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def update_ip(self, request, pk=None):
        vm = self.get_object()
        serializer = VirtualMachineIPSerializer(instance=vm, data=request.data)
        if serializer.is_valid():
            updated_vm = serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def assign_ip_to_vm(self, vm_id, ip_address):
        try:
            vm = VirtualMachine.objects.get(id=vm_id)
            vm.add_ip_address(ip_address)
            return True, "Adresse IP attribuée avec succès."
        except VirtualMachine.DoesNotExist:
            return False, "Machine virtuelle non trouvée."

    def remove_ip_from_vm(self, vm_id, ip_address):
        try:
            vm = VirtualMachine.objects.get(id=vm_id)
            vm.remove_ip_address(ip_address)
            return True, "Adresse IP retirée avec succès."
        except VirtualMachine.DoesNotExist:
            return False, "Machine virtuelle non trouvée."
