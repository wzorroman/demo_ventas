from django.contrib import admin

from apps.base.models.models import Producto


# Register your models here.
@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "descripcion",
        "cantidad",
        "precio",
        "total",
        "date_format",
        "date_created_format",
    )
    search_fields = ("id", "descripcion")
    date_hierarchy = 'fecha_creacion'

    def date_created_format(self, obj):
        return obj.fecha_creacion.strftime("%d/%m/%Y %H:%M:%S") if obj.fecha_creacion else "-"

    date_created_format.short_description = "Created at"

    def date_format(self, obj):
        return obj.fecha.strftime("%d/%m/%Y %H:%M:%S") if obj.fecha else "-"

    date_format.short_description = "Fecha"
