from django.db import models

from .defaults import ATTR_OPTIONS_DEFAULT


class State(models.Model):
    name = models.CharField(verbose_name='Name', max_length=128, unique=True)
    name_readable = models.CharField(verbose_name='Readable name', max_length=128, unique=True)
    is_a = models.ForeignKey('State', verbose_name='Parent Concept', on_delete=models.CASCADE, blank=True, null=True)
    time_added = models.DateTimeField(verbose_name="Time Added", auto_now_add=True)
    time_updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)

    def __str__(self):
        return f'State<{self.name_readable}>'


class Attr(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Name', max_length=128, unique=False)
    name_readable = models.CharField(verbose_name='Readable name', max_length=128, unique=False)
    options = models.TextField(verbose_name='Attr options', default=ATTR_OPTIONS_DEFAULT, blank=True, null=True)
    time_added = models.DateTimeField(verbose_name="Time Added", auto_now_add=True)
    time_updated = models.DateTimeField(verbose_name="Time Updated", auto_now=True)

    class Meta:
        unique_together = ('state', 'name')

    def __str__(self):
        return f'Attr<{self.name_readable}>'

