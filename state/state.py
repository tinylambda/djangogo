import typing
import random
import string
import json

from .models import State
from .models import Attr
from config.models import CommonConfig


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


class StateBase:
    STATE_PREFIX = 'state__'
    STATE_ATTR_PREFIX = 'attr__'

    def __init__(self):
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
        pass

    def deserialize(self, data: typing.Dict):
        """
        Deserialize from existing instance data
        """
        pass

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


class States:
    @classmethod
    def __state_class_name__(cls, name: str):
        return f'{StateBase.STATE_PREFIX}{name}'

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
        is_a: State = state_db_object.is_a

        if is_a is None:
            bases = (StateBase, )
        else:
            parent_cls = cls._load_state_class(is_a)
            bases = (parent_cls, StateBase)

        class_dict: typing.Dict = {
            'name': name,
            'name_readable': name_readable,
        }
        state_class = type(name, bases, class_dict)
        # Update attrs of this concept
        attr_db_objects = state_db_object.attr_set.all()
        for attr_db_object in attr_db_objects:
            attr_class = cls._load_attr_class(attr_db_object)
            attr_name = attr_db_object.name
            setattr(
                state_class,
                f'{StateBase.STATE_ATTR_PREFIX}{attr_name}',
                attr_class
            )

        # Update configs of this concept
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

        cls_dict = {}
        option_type = options.get('type')
        option_default = options.get('default')
        option_container = options.get('container')
        option_container_config: typing.Dict = options.get('container_config')

        cls_dict.update({
            'name': name,
            'name_readable': name_readable,
            'option_type': option_type,
            'option_default': option_default,
            'option_container': option_container,
            'option_container_config': option_container_config,
        })

        attr_cls = type(name, (AttrBase, ), cls_dict)
        return attr_cls
