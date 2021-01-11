from django.contrib import admin

from .models import CommonConfig


@admin.register(CommonConfig)
class CommonConfigAdmin(admin.ModelAdmin):
    pass

