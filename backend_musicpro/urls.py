"""
URL configuration for backend_musicpro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import ProductoListAPI, ProductoDetailAPI, OrdenPedidoList, ProductList, StockList, ProductoList, ProductoDetail, StockDetail, OrdenPedidoCreateAPI, ReducirStockProducto, DetalleOrdenPedidoCreateAPI, DetalleOrdenPedidoListAPI, DetalleOrdenPedidoDetailAPI, ReducirStockProductos
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/products/', ProductoListAPI.as_view(), name='productos-list'),  #No funciona por permisos
    path('api/products/<int:pk>/', ProductoDetailAPI.as_view(), name='productos-detail'),  #No funciona por permisos
    path('api/ordenes-pedido/', OrdenPedidoList.as_view(), name='orden-pedido-list'),
    path('api/productos/list/', ProductList.as_view(), name='product-list'),
    path('api/stock/', StockList.as_view(), name='stock-list'),
    path('api/productos/', ProductoList.as_view(), name='producto-list'),
    path('api/productos/<int:pk>/', ProductoDetail.as_view(), name='producto-detail'),
    path('api/stock/consulta/<int:pk>/', StockDetail.as_view(), name='stock-detail'), 
    path('api/ordenes-pedido/create/', OrdenPedidoCreateAPI.as_view(), name='ordenes-pedido-create'),
    path('api/reducir-stock/', ReducirStockProducto.as_view(), name='reducir_stock'),
    path('api/detalle-orden-pedido/create/', DetalleOrdenPedidoCreateAPI.as_view(), name='detalle-orden-pedido-create'),
    path('api/detalle-orden-pedido/list/', DetalleOrdenPedidoListAPI.as_view(), name='detalle-orden-pedido-list'),
    path('api/detalle-orden-pedido/<int:pk>/', DetalleOrdenPedidoDetailAPI.as_view(), name='detalle-orden-pedido-detail'),
    path('api/reducir-stocks/productos/', ReducirStockProductos.as_view(), name='reducir_stock_productos'),
]
