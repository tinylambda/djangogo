from django.contrib import admin

from .models import Concept
from .models import Attr

from config.models import CommonConfig


class AttrInline(admin.TabularInline):
    model = Attr
    extra = 0
    fields = ('name_readable', 'name', 'options')
    ordering = ('time_added', )
    show_full_result_count = True,
    show_change_link = True


class CommonConfigInline(admin.TabularInline):
    model = CommonConfig
    extra = 0
    fields = ('config_id', 'config')
    ordering = ('time_added',)
    show_full_result_count = True,
    show_change_link = True


@admin.register(Concept)
class ConceptAdmin(admin.ModelAdmin):
    inlines = [
        AttrInline,
        CommonConfigInline,
    ]
    fields = ('name_readable', 'name', 'is_a',)
    list_display = ('name_readable', 'name', 'is_a',)
    search_fields = ('name_readable', 'name', 'is_a__name_readable')
    ordering = ('-time_added', )
    show_full_result_count = True

