from django.contrib import admin

from .models import ConfigRule


@admin.register(ConfigRule)
class ConfigRuleAdmin(admin.ModelAdmin):
    pass

