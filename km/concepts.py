import time
import random
import string
import json
import typing
import logging

from .models import Concept
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
    def get_proto(cls):
        option_default = cls.option_default

        if cls.option_container:
            if cls.option_container not in cls.BUILTIN_CONTAINER_TYPES:
                raise RuntimeError(f'Unsupported container type {cls.option_container}')
            if cls.option_container == 'map':
                return {}
            elif cls.option_container == 'list':
                return []
        else:
            if cls.option_type not in cls.BUILTIN_BASE_TYPES:
                raise RuntimeError(f'Unsupported builtin type <{cls.option_type}>')
            if cls.option_type == 'string':
                return str(option_default) if option_default else ''
            elif cls.option_type == 'int':
                return int(option_default) if option_default else 0
            elif cls.option_type == 'float':
                return float(option_default) if option_default else 0.0
            elif cls.option_type == 'boolean':
                return option_default if option_default is True else False

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
    def is_valid_attribute(cls, instance):
        if cls.option_container:
            if cls.option_container == 'map':
                assert isinstance(instance, dict)
            elif cls.option_container == 'list':
                assert isinstance(instance, list)
        else:
            if cls.option_type == 'string':
                assert isinstance(instance, str)
            elif cls.option_type == 'int':
                assert isinstance(instance, int)
            elif cls.option_type == 'float':
                assert isinstance(instance, float)
            elif cls.option_type == 'boolean':
                assert isinstance(instance, bool)
        return True


class ConceptBase:
    ATTR_PREFIX = 'attr__'

    @classmethod
    def get_attribute_classes(cls):
        attribute_classes = []
        for item in dir(cls):
            if item.startswith(cls.ATTR_PREFIX):
                item_value = getattr(cls, item)
                assert issubclass(item_value, AttrBase)
                attribute_classes.append(item_value)
        return attribute_classes

    @classmethod
    def get_attribute_class(cls, name):
        try:
            attribute_class = getattr(cls, f'{cls.ATTR_PREFIX}{name}')
        except AttributeError:
            raise RuntimeError(f'Unknown attribute <{name}> in concept <{cls.name_readable}>')
        else:
            return attribute_class

    @classmethod
    def get_proto(cls) -> typing.Dict:
        proto = {}
        for attribute_class in cls.get_attribute_classes():
            proto.update({attribute_class.name: attribute_class.get_proto()})
        return proto

    @classmethod
    def new_instance(cls, config_id=None, supplied_instance_id=None):
        instance = cls()
        if supplied_instance_id is not None:
            instance_id = supplied_instance_id
        else:
            assert config_id in cls.configs
            ts = int(time.time())
            rand_str = ''.join(
                random.sample(string.ascii_letters + string.digits, 6)
            )
            instance_id = f'{config_id}-{ts}-{rand_str}'
        instance.config_id = config_id
        instance.instance_id = instance_id
        instance.create_ts = ts
        return instance

    @classmethod
    def get_config(cls, config_id):
        return cls.configs.get(config_id)

    @classmethod
    def is_concept(cls, name):
        try:
            concept = Concepts.get_concept_cls(name)
        except RuntimeError:
            concept = None

        if concept:
            return True
        else:
            return False

    def __init__(self):
        self.instance_id = None  # id for this concept instance
        self.config_id = None
        self.create_ts = None
        self.concept_data = self.get_proto()  # proto as default data

    @classmethod
    def load_concept_instance(cls, concept_instance_data: dict):
        concept_instance = cls()
        assert 'instance_id' in concept_instance_data
        instance_id = concept_instance_data.get('instance_id')
        concept_instance.instance_id = instance_id
        concept_instance.concept_data = concept_instance_data

        attribute_classes = cls.get_attribute_classes()
        for attribute_class in attribute_classes:
            name = attribute_class.get_name()
            attribute_instance_data = concept_instance.concept_data.get(name)
            cls.load_attribute_instance(attribute_class, attribute_instance_data)

    @classmethod
    def load_attribute_instance(cls, attribute_class, attribute_instance_data):
        logging.error(f'Load attribute <{attribute_class.get_name()}> for concept <{cls.name_readable}>')
        logging.error(f'the data is {attribute_instance_data}')

    def serialize(self) -> dict:
        if 'instance_id' not in self.concept_data:  # New created instance
            self.concept_data.update({
                'instance_id': self.instance_id,
                'config_id': self.config_id,
                'create_ts': self.create_ts,
            })
        return self.concept_data


class Concepts:
    @classmethod
    def __concept_cls_name__(cls, name):
        return f'concept__{name}'

    @classmethod
    def load(cls):
        concept_db_objects: typing.List[Concept] = Concept.objects.all()
        for concept_db_object in concept_db_objects:
            concept_cls = cls._load_concept(concept_db_object)
            concept_cls_name = cls.__concept_cls_name__(concept_cls.__name__)
            setattr(cls, concept_cls_name, concept_cls)

    @classmethod
    def get_concept_cls(cls, name):
        concept_cls_name = cls.__concept_cls_name__(name)
        try:
            concept_cls = getattr(cls, concept_cls_name)
        except AttributeError:
            raise RuntimeError(f'Unknown concept <{name}>')
        else:
            return concept_cls

    @classmethod
    def _load_concept(cls, concept: Concept):
        name = concept.name
        name_readable = concept.name_readable
        is_a: Concept = concept.is_a

        if is_a is None:
            bases = (ConceptBase, )
        else:
            parent_cls = cls._load_concept(is_a)
            bases = (parent_cls, ConceptBase)
        cls_dict: typing.Dict = {
            'name': name,
            'name_readable': name_readable,
        }
        concept_cls = type(name, bases, cls_dict)

        # Update attrs of this concept
        attr_db_objects = concept.attr_set.all()
        for attr_db_object in attr_db_objects:
            attr_cls = cls._load_attr(attr_db_object)
            setattr(
                concept_cls,
                f'{ConceptBase.ATTR_PREFIX}{attr_db_object.name}',
                attr_cls
            )

        # Update configs of this concept
        config_db_objects: typing.List[CommonConfig] = concept.commonconfig_set.all()
        configs = {}
        for config_db_object in config_db_objects:
            config_body = json.loads(config_db_object.config)
            configs.update({
                config_db_object.config_id: config_body
            })
        setattr(concept_cls, 'configs', configs)

        return concept_cls

    @classmethod
    def _load_attr(cls, attr: Attr):
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
