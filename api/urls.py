from django.urls import path
from . import views

urlpatterns = [
    path('virtual-machines/', views.VirtualMachineListCreateAPIView.as_view(), name='virtual-machine-list-create'),
    path('virtual-machines/<uuid:pk>/', views.VirtualMachineDetailAPIView.as_view(), name='virtual-machine-detail'),
    # Ajoutez d'autres URL au besoin
]
