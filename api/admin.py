from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Producto, OrdenPedido, DetalleOrdenPedido

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email', 'role']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )

admin.site.register(OrdenPedido)
admin.site.register(DetalleOrdenPedido)
admin.site.register(Producto)
admin.site.register(CustomUser)
admin.site.site_header = "Administración de Bodega"
admin.site.site_title = "Administración de Bodega"
admin.site.index_title = "Bienvenido al sistema de administración de bodega"