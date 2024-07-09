import os
import django
import requests
from api.models import VirtualMachine, UsageHistory  

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')  
django.setup()

def get_firecracker_usage(vm):
    # Remplacez par l'URL de l'API Firecracker pour cette VM
    url = f"http://{vm.network_interfaces.first().ip_address}:8080/metrics"
    response = requests.get(url)
    data = response.json()

    cpu_usage = data['cpu_usage_percent']
    memory_usage = data['memory_usage_percent']
    disk_usage = data['disk_usage_percent']
    return {
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'disk_usage': disk_usage,
    }

def collect_usage_data():
    vms = VirtualMachine.objects.filter(status='running')
    for vm in vms:
        usage = get_firecracker_usage(vm)
        UsageHistory.objects.create(
            vm=vm,
            cpu_usage=usage['cpu_usage'],
            memory_usage=usage['memory_usage'],
            disk_usage=usage['disk_usage'],
        )

if __name__ == "__main__":
    collect_usage_data()
