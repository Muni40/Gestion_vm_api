from django.db import models
from django.contrib.auth.models import User

class CPU(models.Model):
    id = models.AutoField(primary_key=True)
    cores = models.IntegerField()

    def __str__(self):
        return f"{self.cores} cores"

class Memory(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.IntegerField()  # in MB

    def __str__(self):
        return f"{self.size} MB"

class Disk(models.Model):
    class Types(models.TextChoices):
        SSHD = 'sshd'
        HDD = 'hdd'
        SSD = 'ssd'
    id = models.AutoField(primary_key=True)
    size = models.IntegerField()  # in GB
    type = models.CharField(max_length=50, choices=Types.choices)  

    def __str__(self):
        return f"{self.size} GB {self.type}"

class NetworkInterface(models.Model):
    id = models.AutoField(primary_key=True)
    ip_address = models.CharField(max_length=15)
    mac_address = models.CharField(max_length=17)

    def __str__(self):
        return f"IP: {self.ip_address}, MAC: {self.mac_address}"

class OperatingSystem(models.Model):
    id = models.AutoField(primary_key=True)
    os_type = models.CharField(max_length=50)
    os_version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.os_type} {self.os_version}"

class VirtualMachine(models.Model):
    class VMStatus(models.TextChoices):
        RUNNING = 'running'
        STOPPED = 'stopped'

    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cpu = models.ForeignKey(CPU, on_delete=models.CASCADE)
    memory = models.ForeignKey(Memory, on_delete=models.CASCADE)
    disk = models.ForeignKey(Disk, on_delete=models.CASCADE)
    network_interfaces = models.ForeignKey(NetworkInterface, on_delete=models.CASCADE)
    os = models.ForeignKey(OperatingSystem, on_delete=models.CASCADE)
    status = models.CharField(max_length=50,choices=VMStatus.choices)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #  monitoring and management
    cpu_usage = models.FloatField(default=0.0,editable=False)  # in percentage
    memory_usage = models.FloatField(default=0.0,editable=False)  # in percentage
    disk_usage = models.FloatField(default=0.0,editable=False)  # in percentage
    ip_addresses = models.CharField(max_length=255, blank=True, default="", editable=False)# IPs separated by commas

    def __str__(self):
        return self.name
    
    def add_ip_address(self, ip_address):
        if ip_address not in self.ip_addresses.split(","):
            if self.ip_addresses:
                self.ip_addresses += f",{ip_address}"
            else:
                self.ip_addresses = ip_address
            self.save()

    def remove_ip_address(self, ip_address):
        ip_list = self.ip_addresses.split(",")
        if ip_address in ip_list:
            ip_list.remove(ip_address)
            self.ip_addresses = ",".join(ip_list)
            self.save()

    def update_ip_addresses(self, new_ip_addresses):
        self.ip_addresses = ",".join(new_ip_addresses)
        self.save()

    
class UsageHistory(models.Model):
    id = models.AutoField(primary_key=True)
    vm = models.ForeignKey(VirtualMachine, on_delete=models.CASCADE,editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField(default=0,editable=False)
    memory_usage = models.FloatField(default=0,editable=False)
    disk_usage = models.FloatField(default=0,editable=False)

    def __str__(self):
        return f"Usage at {self.timestamp} for VM {self.vm.name}"