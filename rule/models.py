from django.db import models

from .defaults import RULE_DEFAULT
from .defaults import INPUT_KEYS_DEFAULT
from .defaults import OUTPUT_KEYS_DEFAULT


class ConfigRule(models.Model):
    input_keys = models.TextField(verbose_name='Input Keys', default=INPUT_KEYS_DEFAULT)
    output_keys = models.TextField(verbose_name='Output Keys', default=OUTPUT_KEYS_DEFAULT)
    rules = models.TextField(verbose_name='Rules', default=RULE_DEFAULT)
    time_added = models.DateTimeField(verbose_name="Time Added", auto_now_add=True)
    time_updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)

    def __str__(self):
        return f'ConfigRule<{self.output_keys}>'


class ConstraintRule(models.Model):
    pass

