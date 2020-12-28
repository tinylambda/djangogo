import json
import typing

from .models import Concept
from .models import Attr


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
    def get_proto(cls):
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
                return ''
            elif cls.option_type == 'int':
                return 0
            elif cls.option_type == 'float':
                return 0.0
            elif cls.option_type == 'boolean':
                return False

    @classmethod
    def get_type(cls):
        return cls.option_type


class ConceptBase:
    ATTR_PREFIX = 'attr__'

    def __init__(self):
        self.data = {}

    @classmethod
    def get_attributes(cls):
        attributes = []
        for item in dir(cls):
            if item.startswith(cls.ATTR_PREFIX):
                item_value = getattr(cls, item)
                assert issubclass(item_value, AttrBase)
                attributes.append(item_value)
        return attributes

    @classmethod
    def get_proto(cls) -> typing.Dict:
        proto = {}
        for attribute in cls.get_attributes():
            proto.update({attribute.name: attribute.get_proto()})
        return proto

    @classmethod
    def instance(cls):
        return cls()

    def deserialization(self, data: dict):
        pass

    def serialization(self) -> dict:
        pass


class Concepts:
    @classmethod
    def __concept_cls_name__(cls, name):
        return f'concept__{name}'

    @classmethod
    def load(cls):
        concept_db_objects: typing.List[Concept] = Concept.objects.all()
        for concept_db_object in concept_db_objects:
            concept_cls = cls._load_concept(concept_db_object.name)
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
    def _load_concept(cls, concept_name: str):
        concept = Concept.objects.get(name=concept_name)
        name = concept.name
        name_readable = concept.name_readable
        is_a: Concept = concept.is_a

        if is_a is None:
            bases = (ConceptBase, )
        else:
            parent_cls = cls._load_concept(is_a.name)
            bases = (parent_cls, ConceptBase)
        cls_dict: typing.Dict = {
            'name': name,
            'name_readable': name_readable,
        }
        concept_cls = type(name, bases, cls_dict)

        for attr in concept.attr_set.all():
            attr_cls = cls._load_attr(attr)
            setattr(
                concept_cls,
                f'{ConceptBase.ATTR_PREFIX}{attr.name}',
                attr_cls
            )

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
