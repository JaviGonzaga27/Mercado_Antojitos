from rest_framework import viewsets
from .models import Venta
from .serializers import VentaSerializer
import requests

class VentaViewSet(viewsets.ModelViewSet):
    queryset = Venta.objects.all()
    serializer_class = VentaSerializer

    def perform_create(self, serializer):
        venta = serializer.save()
        self.actualizar_inventario(venta)

    def actualizar_inventario(self, venta):
        for detalle in venta.detalles.all():
            url = f"http://inventario-service:8000/api/productos/{detalle.producto_id}/"
            data = {"cantidad": -detalle.cantidad}
            requests.patch(url, data=data)