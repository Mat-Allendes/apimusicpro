from rest_framework import serializers
from .models import CustomUser, Producto, OrdenPedido, DetalleOrdenPedido

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

class OrdenPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrdenPedido
        fields = '__all__'
    
    producto_id = serializers.IntegerField(write_only=True)
    cantidad_venta = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        detalles_data = validated_data.pop('detalleordenpedido_set')
        orden_pedido = OrdenPedido.objects.create(**validated_data)
        for detalle_data in detalles_data:
            DetalleOrdenPedido.objects.create(orden_pedido=orden_pedido, **detalle_data)
        return orden_pedido
    
class DetalleOrdenPedidoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetalleOrdenPedido
        fields = '__all__'

class ProductoStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'stock']

class ProductoDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'