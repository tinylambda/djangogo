from django.contrib import admin

from .models import State
from .models import Attr


class AttrInline(admin.TabularInline):
    model = Attr
    extra = 0
    fields = ('name_readable', 'name', 'options')
    ordering = ('time_added', )
    show_full_result_count = True,
    show_change_link = True


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    inlines = [
        AttrInline,
    ]
    fields = ('name_readable', 'name', 'is_a',)
    list_display = ('name_readable', 'name', 'is_a',)
    search_fields = ('name_readable', 'name', 'is_a__name_readable')
    ordering = ('-time_added', )
    show_full_result_count = True

