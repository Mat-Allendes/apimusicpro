from django.shortcuts import render
from .models import CustomUser, Producto, OrdenPedido, DetalleOrdenPedido
from rest_framework import generics
from .serializers import ProductoSerializer, OrdenPedidoSerializer, DetalleOrdenPedidoSerializer, ProductoStockSerializer, ProductoDetailSerializer
from guardian.shortcuts import get_objects_for_user
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.views import APIView



# Create your views here.

class ProductoListAPI(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ProductoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

class OrdenPedidoList(generics.ListAPIView):
    queryset = OrdenPedido.objects.all()
    serializer_class = OrdenPedidoSerializer

    def post(self, request, *args, **kwargs):
        producto_id = request.data.get('producto_id')
        cantidad_venta = request.data.get('cantidad_venta')
        
        try:
            producto = Producto.objects.get(id=producto_id)
            
            if producto.stock >= int(cantidad_venta):
                producto.stock -= int(cantidad_venta)
                producto.save()
                
                orden_pedido = OrdenPedido.objects.create(usuario=request.user)
                DetalleOrdenPedido.objects.create(orden_pedido=orden_pedido, producto=producto, cantidad=cantidad_venta)
                
                return Response({'detail': 'Venta realizada exitosamente.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'No hay suficiente stock para realizar la venta.'}, status=status.HTTP_400_BAD_REQUEST)
        except Producto.DoesNotExist:
            return Response({'detail': 'El producto no existe.'}, status=status.HTTP_400_BAD_REQUEST)

class StockList(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoStockSerializer

class ProductList(generics.ListAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoDetailSerializer
    
    def perform_create(self, serializer):
        instance = serializer.save()
        for detalle in instance.detalleordenpedido_set.all():
            producto = detalle.producto
            producto.stock -= detalle.cantidad
            producto.save()

#vistas para consultar datos, reduccion de stock, creacion de ordenes de pedido y CRUD de productos
class ProductoList(generics.ListCreateAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoDetailSerializer

class ProductoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoDetailSerializer

class StockDetail(generics.RetrieveAPIView):
    queryset = Producto.objects.all()
    serializer_class = ProductoStockSerializer

#FUNCIONAAAAAA!!!
class OrdenPedidoCreateAPI(generics.CreateAPIView):
    def post(self, request):
        detalle_orden_pedido_ids = request.data.get('detalle_orden_pedido_id', [])
        cantidad = request.data.get('cantidad')
        
        if not isinstance(detalle_orden_pedido_ids, list):
            detalle_orden_pedido_ids = [detalle_orden_pedido_ids]
        
        for detalle_orden_pedido_id in detalle_orden_pedido_ids:
            detalle_orden_pedido = get_object_or_404(DetalleOrdenPedido, id=detalle_orden_pedido_id)
            producto = detalle_orden_pedido.producto
            
            if producto.stock >= int(cantidad):
                producto.stock -= int(cantidad)
                producto.save()
            else:
                return Response({'error': 'No hay suficiente stock disponible para reducir.'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'message': 'Stock reducido correctamente.'}, status=status.HTTP_200_OK)

#FUNCIONA!!!!
class ReducirStockProducto(APIView):
    def post(self, request):
        id_producto = request.data.get('id')
        cantidad_vendida = request.data.get('cantidad')
        
        try:
            producto = Producto.objects.get(id=id_producto)
            
            if producto.stock >= int(cantidad_vendida):
                producto.stock -= int(cantidad_vendida)
                producto.save()
                
                return Response({'message': 'Stock reducido correctamente.'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No hay suficiente stock disponible para reducir.'}, status=status.HTTP_400_BAD_REQUEST)
        
        except Producto.DoesNotExist:
            return Response({'error': 'El producto no existe.'}, status=status.HTTP_404_NOT_FOUND)

#funciona!!!
class DetalleOrdenPedidoCreateAPI(generics.CreateAPIView):
    queryset = DetalleOrdenPedido.objects.all()
    serializer_class = DetalleOrdenPedidoSerializer

class DetalleOrdenPedidoListAPI(generics.ListAPIView):
    queryset = DetalleOrdenPedido.objects.all()
    serializer_class = DetalleOrdenPedidoSerializer

class DetalleOrdenPedidoDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = DetalleOrdenPedido.objects.all()
    serializer_class = DetalleOrdenPedidoSerializer

class ReducirStockProductos(APIView):
    def post(self, request):
        producto_ids = request.data.get('producto_ids')
        cantidad = request.data.get('cantidad')
        
        try:
            productos = Producto.objects.filter(id__in=producto_ids)
            
            for producto in productos:
                if producto.stock >= int(cantidad):
                    producto.stock -= int(cantidad)
                    producto.save()
                else:
                    return Response({'error': f'No hay suficiente stock disponible para reducir el producto {producto.nombre}.'}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({'message': 'Stock reducido correctamente.'}, status=status.HTTP_200_OK)
        
        except Producto.DoesNotExist:
            return Response({'error': 'Uno o más productos no existen.'}, status=status.HTTP_404_NOT_FOUND)