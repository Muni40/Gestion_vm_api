from django.contrib.auth.models import User
from django.db import models

class CPU(models.Model):
    cores = models.IntegerField()

    def __str__(self):
        return f"{self.cores} cores"

class Memory(models.Model):
    size = models.IntegerField()  # in MB

    def __str__(self):
        return f"{self.size} MB"

class Disk(models.Model):
    size = models.IntegerField()  # in GB

    def __str__(self):
        return f"{self.size} GB"

class NetworkInterface(models.Model):
    ip_address = models.CharField(max_length=15)
    mac_address = models.CharField(max_length=17)

    def __str__(self):
        return f"IP: {self.ip_address}, MAC: {self.mac_address}"

class OperatingSystem(models.Model):
    os_type = models.CharField(max_length=50)
    os_version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.os_type} {self.os_version}"

class VirtualMachine(models.Model):
    name = models.CharField(max_length=100)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
    network_interfaces = models.ManyToManyField(NetworkInterface)
    os = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='stopped')  # e.g., running, stopped
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
