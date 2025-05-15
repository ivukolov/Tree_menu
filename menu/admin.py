from django.contrib import admin
from .models import MenuItem
from django.db.models import Q


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1
    fields = ('name', 'menu_name', 'named_url', 'url', 'order')


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'menu_name', 'order', 'get_url')
    list_filter = ('menu_name',)
    search_fields = ('name', 'menu_name')
    inlines = [MenuItemInline]

    # Оставляем только элементы с подменю
    def get_queryset(self, request):
        queryset = super().get_queryset(request).filter(
            Q(parent__isnull=True) | (Q(parent__isnull=False) & Q(
                children__isnull=False
            ))
        ).select_related('parent').distinct()
        print(queryset)
        return queryset
