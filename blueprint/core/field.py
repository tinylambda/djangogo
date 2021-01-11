import typing

from weakref import WeakKeyDictionary

from blueprint.core.checker import Checker


class Field:
    TYPES = (
        'string',
        'int',
        'float',
        'boolean',
    )
    CONTAINERS = (
        'map',
        'list',
    )

    def __init__(
            self,
            verbose_name: str = None,
            data_type: typing.Any = 'string',
            required: bool = True,
            default: typing.Any = None,
            container: str = None,
            container_config: dict = {},
    ):
        self.name = None
        self.verbose_name = verbose_name
        self.data_type: str = data_type
        self.required: bool = required
        self.default: typing.Any = default
        self.container: str = container
        self.container_config: dict = container_config

        if self.container == 'map' and self.default is None:
            self.default = self.default if self.default else {}
        if self.container == 'list' and self.default is None:
            self.default = self.default if self.default else []

        self._values: WeakKeyDictionary = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        value = self._values.get(instance)
        value = value if value is not None else self.default
        return value

    def __set__(self, instance, value):
        blueprint_name = instance.__class__.__name__.lower()
        blueprint_context = instance.build_context()
        full_field_name = f'{blueprint_name}.{self.name}'

        # Check before changing value
        # Raise exception here to indicate invalid state error
        Checker.check(full_field_name, value, blueprint_context)

        # Value of field check pass, now can store the latest value
        value = value if value is not None else self.default
        self._values[instance] = value

