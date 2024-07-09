# urls.py
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'cpus', CPUViewSet)
router.register(r'memories', MemoryViewSet)
router.register(r'disks', DiskViewSet)
router.register(r'network-interfaces', NetworkInterfaceViewSet)
router.register(r'operating-systems', OperatingSystemViewSet)
router.register(r'virtual-machines', VirtualMachineViewSet)
router.register(r'usage-history', UsageHistoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('virtual-machines/<int:pk>/assign_ip/', VirtualMachineViewSet.as_view({'post & get': 'assign_ip'}), name='assign_ip'),
    path('virtual-machines/<int:pk>/remove_ip/', VirtualMachineViewSet.as_view({'post': 'remove_ip'}), name='remove_ip'),
]
