import typing
import json

from .models import State
from .models import Attr
from .base import AttrBase, StateBase
from config.models import CommonConfig


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
        # Update attrs of this concept
        attr_db_objects = state_db_object.attr_set.all()
        for attr_db_object in attr_db_objects:
            attr_class = cls._load_attr_class(attr_db_object)
            attr_name = attr_db_object.name
            attr_instance = attr_class()
            setattr(
                state_class,
                f'{StateBase.STATE_ATTR_PREFIX}{attr_name}',
                attr_instance
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
