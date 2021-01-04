import time
import random
import string
import typing

from weakref import WeakKeyDictionary


class AttrChecker:
    pass


class AttrBase:
    BUILTIN_BASE_TYPES = (
        'string',
        'int',
        'float',
        'boolean',
    )
    BUILTIN_CONTAINER_TYPES = (
        'map',
        'list',
    )

    @classmethod
    def get_name(cls):
        return cls.name

    @classmethod
    def get_name_readable(cls):
        return cls.name_readable

    @classmethod
    def get_data_type(cls):
        return cls.option_type

    @classmethod
    def get_container(cls):
        return cls.option_container

    @classmethod
    def get_container_config(cls):
        return cls.option_container_config

    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance)

    def __set__(self, instance, value):
        # Check according to the configured rules
        self._values[instance] = value

    def serialize(self):
        pass

    def deserialize(self):
        pass


class StateBase:
    STATE_PREFIX = 'state__'
    STATE_ATTR_PREFIX = 'attr__'

    def __init__(self):
        self.buffer_info: dict = {}
        self.config_id = None
        self.instance_id: str = None
        self.create_ts: int = None
        self.instance_id_template = None

    @property
    def random_str(self):
        data = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        return data

    def serialize(self) -> typing.Dict:
        """
        Serialize existing instance or newly created instance to a dictionary
        """
        print('in serialize', self)

    def deserialize(self, data: typing.Dict):
        """
        Deserialize from existing instance data
        """
        instance_id: str = data.get('instance_id')
        if instance_id is None:
            raise RuntimeError('instance_id should not be None')
        self.instance_id = instance_id
        self.create_ts = data.get('create_ts', int(time.time()))

    def get_config(self) -> typing.Dict:
        config: dict = self.configs.get(self.config_id)
        return config

    @classmethod
    def __attribute_class_name__(cls, name):
        return f'{cls.STATE_ATTR_PREFIX}{name}'

    @classmethod
    def get_attribute_class(cls, name: str):
        attribute_name: str = cls.__attribute_class_name__(name)
        try:
            attribute_class = getattr(cls, attribute_name)
        except AttributeError:
            attribute_class = None
        return attribute_class

    @classmethod
    def get_all_attribute_classes(cls):
        attribute_classes = []
        for item in dir(cls):
            if item.startswith(cls.STATE_ATTR_PREFIX):
                item_value = getattr(cls, item)
                assert issubclass(item_value, AttrBase)
                attribute_classes.append(item_value)

        all_attributes = {
            item.name: item
            for item in attribute_classes
        }
        return all_attributes

