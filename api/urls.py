from rest_framework import routers
from .views import ProductoViewSet, OrdenPedidoViewSet, DetalleOrdenPedidoViewSet, StockViewSet, ReducirStockProductosViewSet, ReducirStockProductoViewSet, StockProductoViewSet, DetalleOrdenPedidoCreateAPI, DetalleOrdenPedidoListAPI

router = routers.DefaultRouter()

router.register('productos', ProductoViewSet, 'productos')
router.register('ordenes-pedido', OrdenPedidoViewSet, 'ordenes-pedido')
router.register('detalles-orden-pedido', DetalleOrdenPedidoViewSet, 'detalles-orden-pedido')
router.register('stock', StockViewSet, 'stock')
router.register('stock-producto', StockProductoViewSet, 'stock-producto')
router.register('reducir-stock-productos', ReducirStockProductosViewSet, 'reducir-stock-productos')
router.register('reducir-stock-producto', ReducirStockProductoViewSet, 'reducir-stock-producto')
router.register('detalle-orden-pedido/create', DetalleOrdenPedidoCreateAPI, 'detalle-orden-pedido-create')
router.register('detalle-orden-pedido/list', DetalleOrdenPedidoListAPI, 'detalle-orden-pedido-list')

urlpatterns = router.urls