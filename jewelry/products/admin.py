from django.contrib import admin

from .models import Client, Composition, Jewelry, JewelryType, Material


class CompositionInline(admin.TabularInline):
    model = Composition
    extra = 2


class JewelryAdmin(admin.ModelAdmin):
    list_display = ('title', 'jewelry_type', 'customer', 'get_excerpt', 'materials_list',
                    'weight', 'full_price', 'get_price', 'created_date')
    list_filter = ('jewelry_type',)
    inlines = [CompositionInline]


class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'price')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'phone', 'is_regular', 'discount')


admin.site.register(Jewelry, JewelryAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(JewelryType)
admin.site.register(Client, ClientAdmin)
