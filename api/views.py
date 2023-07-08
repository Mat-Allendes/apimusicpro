from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.response import Response

from .models import CustomUser, Producto, OrdenPedido, DetalleOrdenPedido
from .serializers import (
    ProductoSerializer, OrdenPedidoSerializer, DetalleOrdenPedidoSerializer,
    ProductoStockSerializer, ProductoDetailSerializer
)
from guardian.shortcuts import get_objects_for_user


class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        instance = serializer.save()
        for detalle in instance.detalleordenpedido_set.all():
            producto = detalle.producto
            producto.stock -= detalle.cantidad
            producto.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for detalle in instance.detalleordenpedido_set.all():
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        instance.delete()


class OrdenPedidoViewSet(viewsets.ModelViewSet):
    queryset = OrdenPedido.objects.all()
    serializer_class = OrdenPedidoSerializer

    def create(self, request, *args, **kwargs):
        producto_id = request.data.get('producto_id')
        cantidad_venta = request.data.get('cantidad_venta')
        
        try:
            producto = Producto.objects.get(id=producto_id)
            
            if producto.stock >= int(cantidad_venta):
                producto.stock -= int(cantidad_venta)
                producto.save()
                
                orden_pedido = OrdenPedido.objects.create(usuario=request.user)
                DetalleOrdenPedido.objects.create(
                    orden_pedido=orden_pedido, producto=producto, cantidad=cantidad_venta
                )
                
                return Response(
                    {'detail': 'Venta realizada exitosamente.'}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'detail': 'No hay suficiente stock para realizar la venta.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Producto.DoesNotExist:
            return Response(
                {'detail': 'El producto no existe.'}, status=status.HTTP_400_BAD_REQUEST
            )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def perform_destroy(self, instance):
        for detalle in instance.detalleordenpedido_set.all():
            producto = detalle.producto
            producto.stock += detalle.cantidad
            producto.save()
        instance.delete()


class DetalleOrdenPedidoViewSet(viewsets.ModelViewSet):
    queryset = DetalleOrdenPedido.objects.all()
    serializer_class = DetalleOrdenPedidoSerializer


class StockViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoStockSerializer


class ReducirStockProductosViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        producto_ids = request.data.get('producto_ids')
        cantidad = request.data.get('cantidad')

        try:
            productos = Producto.objects.filter(id__in=producto_ids)

            for producto in productos:
                if producto.stock >= int(cantidad):
                    producto.stock -= int(cantidad)
                    producto.save()
                else:
                    return Response(
                        {'error': f'No hay suficiente stock disponible para reducir el producto {producto.nombre}.'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response({'message': 'Stock reducido correctamente.'}, status=status.HTTP_200_OK)

        except Producto.DoesNotExist:
            return Response({'error': 'Uno o más productos no existen.'}, status=status.HTTP_404_NOT_FOUND)


class ReducirStockProductoViewSet(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        id_producto = request.data.get('id')
        cantidad_vendida = request.data.get('cantidad')

        try:
            producto = Producto.objects.get(id=id_producto)

            if producto.stock >= int(cantidad_vendida):
                producto.stock -= int(cantidad_vendida)
                producto.save()

                return Response({'message': 'Stock reducido correctamente.'}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'error': 'No hay suficiente stock disponible para reducir.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        except Producto.DoesNotExist:
            return Response({'error': 'El producto no existe.'}, status=status.HTTP_404_NOT_FOUND)

class StockProductoViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        producto = Producto.objects.filter(pk=pk).first()
        if producto:
            serializer = ProductoStockSerializer(producto)
            return Response(serializer.data)
        else:
            return Response({'error': 'El producto no existe.'}, status=status.HTTP_404_NOT_FOUND)

class DetalleOrdenPedidoCreateAPI(viewsets.ModelViewSet):
    queryset = DetalleOrdenPedido.objects.all()
    serializer_class = DetalleOrdenPedidoSerializer


class DetalleOrdenPedidoListAPI(viewsets.ReadOnlyModelViewSet):
    queryset = DetalleOrdenPedido.objects.all()
    serializer_class = DetalleOrdenPedidoSerializer