from django.contrib import admin

from .models import MenuModel


@admin.register(MenuModel)
class MenuAdmin(admin.ModelAdmin):
    fields = ('name_menu', 'top_menu', )
    list_display = ('id', 'name_menu', 'position', 'top_menu')
    list_display_links = ('id',)
    list_editable = ('name_menu',)
    list_per_page = 10
    list_select_related = ('top_menu',)
    ordering = ('id',)
    radio_fields = {"top_menu": admin.HORIZONTAL}
    empty_value_display = "Отсутствует"
    raw_id_fields = ["top_menu"]
