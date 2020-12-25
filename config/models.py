from django.db import models

from km.models import Concept

from .defaults import CONFIG_DEFAULT


class CommonConfig(models.Model):
    config_for = models.ForeignKey(Concept, on_delete=models.CASCADE)
    config_id = models.CharField(verbose_name='Config ID', max_length=128, db_index=True)
    config = models.TextField(verbose_name='Configuration', default=CONFIG_DEFAULT)
    time_added = models.DateTimeField(verbose_name="Time Added", auto_now_add=True)
    time_updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)

    class Meta:
        unique_together = ('config_for', 'config_id')

    def __str__(self):
        return f'CommonConfig<{self.config_for.name_readable}, {self.config_id}>'

