from django.db import models

from .defaults import CONFIG_DEFAULT


class CommonConfig(models.Model):
    config_key = models.CharField(verbose_name='Config Key', max_length=128, db_index=True)
    config_id = models.CharField(verbose_name='Config ID', max_length=128, db_index=True)
    config = models.TextField(verbose_name='Configuration', default=CONFIG_DEFAULT)
    time_added = models.DateTimeField(verbose_name="Time Added", auto_now_add=True)
    time_updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)

    class Meta:
        unique_together = ('config_key', 'config_id')

    def __str__(self):
        return f'CommonConfig<{self.config_key}, {self.config_id}>'

