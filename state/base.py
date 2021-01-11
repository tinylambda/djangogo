import time
import json
import logging
import random
import string
import typing

from weakref import WeakKeyDictionary

from .models import State
from .models import Attr

from config.models import CommonConfig
from .checker import Checker


class AttrBase:
    ATTR_PREFIX = 'attr__'

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

    @classmethod
    def instance(cls, **kwargs):
        return cls(**kwargs)

    def __init__(self):
        self._values = WeakKeyDictionary()

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self._values.get(instance)

    def __set__(self, instance, value):
        # Check according to the configured rules
        print(self.fullname, self.fullname_readable, '!!!')
        logging.debug(f'Checking {self.fullname}>{self.fullname_readable} = <{value}>')
        self._values[instance] = value


class StateBase:
    STATE_PREFIX = 'state__'

    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.buffer_info: dict = {}
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
        if self.instance_id is None:
            # Newly created instance, generate instance_id and create_ts
            self.create_ts = int(time.time())

        print('in serialize', self)

    def deserialize(self, data: typing.Dict):
        """
        Deserialize from existing instance data (should contain instance_id)
        """
        instance_id: str = data.get('instance_id')
        if instance_id is None:
            raise RuntimeError('instance_id should not be None')
        self.instance_id = instance_id
        self.create_ts = data.get('create_ts')
        if not self.create_ts:
            ts = int(time.time())
            logging.debug(f'setting create_ts to {ts}')
            self.create_ts = ts

    def get_config(self) -> typing.Dict:
        config: dict = self.configs.get(self.config_id)
        return config

    @classmethod
    def __attribute_instance_name__(cls, name):
        return f'{AttrBase.ATTR_PREFIX}{name}'

    @classmethod
    def get_attribute(cls, name: str):
        attribute_name: str = cls.__attribute_instance_name__(name)
        try:
            attribute_instance = getattr(cls, attribute_name)
        except AttributeError:
            attribute_instance = None
        return attribute_instance

    @classmethod
    def get_all_attributes(cls):
        attribute_instances = []
        for item in dir(cls):
            if item.startswith(AttrBase.ATTR_PREFIX):
                item_value = getattr(cls, item)
                assert isinstance(item_value, AttrBase)
                attribute_instances.append(item_value)

        all_attributes = {
            item.name: item
            for item in attribute_instances
        }
        return all_attributes

    @classmethod
    def instance(cls, **kwargs):
        return cls(**kwargs)

    @classmethod
    def __state_class_name__(cls, name: str):
        return f'{cls.STATE_PREFIX}{name}'

    @classmethod
    def load_all_state_classes(cls):
        state_db_objects: typing.List[State] = State.objects.all()
        for state_db_object in state_db_objects:
            print('loading state class', state_db_object.name_readable)
            state_class = cls._load_state_class(state_db_object)
            state_class_name = cls.__state_class_name__(state_db_object.name)
            setattr(cls, state_class_name, state_class)

    @classmethod
    def get_state_class(cls, name: str):
        state_class_name: str = cls.__state_class_name__(name)
        try:
            state_class = getattr(cls, state_class_name)
        except AttributeError:
            state_class = None
        return state_class

    @classmethod
    def get_all_state_classes(cls):
        state_classes = [
            getattr(cls, item)
            for item in dir(cls)
            if item.startswith(StateBase.STATE_PREFIX)
        ]
        all_state_classes = {item.name: item for item in state_classes}
        return all_state_classes

    @classmethod
    def _load_state_class(cls, state_db_object: State):
        name = state_db_object.name
        name_readable = state_db_object.name_readable
        instance_id_template = state_db_object.instance_id_template
        is_a: State = state_db_object.is_a

        if is_a is None:
            bases = (StateBase, )
        else:
            parent_cls = cls._load_state_class(is_a)
            bases = (parent_cls, StateBase)

        class_dict: typing.Dict = {
            'name': name,
            'name_readable': name_readable,
            'instance_id_template': instance_id_template,
        }
        state_class = type(name, bases, class_dict)

        # Update attrs of this state
        attr_db_objects = state_db_object.attr_set.all()
        for attr_db_object in attr_db_objects:
            attr_class = cls._load_attr_class(attr_db_object)
            attr_name = attr_db_object.name
            attr_instance = attr_class()
            setattr(
                state_class,
                f'{AttrBase.ATTR_PREFIX}{attr_name}',
                attr_instance
            )

        # Update configs of this state
        config_db_objects: typing.List[CommonConfig] = state_db_object.commonconfig_set.all()
        configs = {}
        for config_db_object in config_db_objects:
            config_body = json.loads(config_db_object.config)
            configs.update({
                config_db_object.config_id: config_body
            })
        setattr(state_class, 'configs', configs)

        return state_class

    @classmethod
    def _load_attr_class(cls, attr: Attr):
        name_readable = attr.name_readable
        name = attr.name
        options: typing.Dict = json.loads(attr.options)

        class_dict = {}
        option_type = options.get('type')
        option_default = options.get('default')
        option_container = options.get('container')
        option_container_config: typing.Dict = options.get('container_config')

        class_dict.update({
            'name': name,
            'name_readable': name_readable,
            'fullname': f'{attr.state.name}.state.{attr.name}',
            'fullname_readable': f'{attr.state.name_readable}{attr.name_readable}',
            'option_type': option_type,
            'option_default': option_default,
            'option_container': option_container,
            'option_container_config': option_container_config,
        })

        attr_class = type(name, (AttrBase, ), class_dict)
        return attr_class



