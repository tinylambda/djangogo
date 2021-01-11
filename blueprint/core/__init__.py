import typing
import string
import random
import time

from blueprint.core.field import Field
from blueprint.exceptions import BluePrintException
from .db import DB


class BluePrintMeta(type):
    def __new__(mcs, name, bases, class_dict: dict):
        # Inject instance_id and create_ts field to created class
        # Every instance of a newly created blueprint instance
        # should generate a instance id and record created timestamp
        instance_id = Field(
            verbose_name='Instance ID',
            data_type='string',
            required=True,
        )

        create_ts = Field(
            verbose_name='Create Timestamp',
            data_type='int',
            required=True,
        )

        class_dict.update({
            'instance_id': instance_id,
            'create_ts': create_ts,
        })

        # Fill the name attribute of all field instances
        for key, value in class_dict.items():
            if isinstance(value, Field):
                # Fill the name attribute
                value.name = key
                # verbose_name default to name
                if value.verbose_name is None:
                    value.verbose_name = value.name

        # Meta context of this blueprint class definition
        meta_context: dict = {}
        meta_class = class_dict.get('Meta')
        if meta_class:
            meta_dict: dict = meta_class.__dict__
            for meta_k, meta_v in meta_dict.items():
                if not meta_k.startswith('__'):
                    meta_context.update({
                        meta_k: meta_v,
                    })

        # __init__ method of each blueprint class
        def init(self, **kwargs):
            cls_dict: dict = self.__class__.__dict__
            for k, v in cls_dict.items():
                # Initialize blueprint instance by user provided arguments
                if isinstance(v, Field):
                    if k in kwargs:
                        user_supplied_value = kwargs.get(k)
                        setattr(self, k, user_supplied_value)

            _meta_context = cls_dict.get('meta_context')
            # Ensure that instance_id_template exists in meta_context
            instance_id_template = _meta_context.get('instance_id_template')
            if not instance_id_template:
                raise BluePrintException(
                    msg='You should specify instance_id_template in Meta section of each blueprint'
                        'to set how to create the instance_id of each blueprint instance'
                )
            # Get create_ts
            self.create_ts = int(time.time())

            # Generate a instance_id according to the instance_id_template
            render_context = self._serialize(validate=False)
            render_context.pop('instance_id')
            self.instance_id = instance_id_template.format(random_string=self.random_string, **render_context)

        def build_render_context(self):
            pass

        # Update class dict
        class_dict.update({
            'instance_id': instance_id,
            'create_ts': create_ts,

            'meta_context': meta_context,

            '__init__': init,
        })

        cls = type.__new__(mcs, name, bases, class_dict)
        return cls


class BluePrint(metaclass=BluePrintMeta):
    def save(self):
        data = self._serialize()
        print('Saving: ', data)

    def get(self):
        pass

    def build_context(self) -> typing.Dict:
        print(self)
        return {}

    @property
    def random_string(self):
        r = ''.join(random.sample(string.ascii_letters + string.digits, 6))
        return r

    def validate_field(self, f: Field):
        field_value = getattr(self, f.name)

        if type(f.data_type) is BluePrintMeta and issubclass(f.data_type, BluePrint):
            pass

        if f.container:
            if f.container == 'map':
                assert isinstance(field_value, dict)
            elif f.container == 'list':
                assert isinstance(field_value, list)
            else:
                assert False, 'No such container type <%s>' % f.container
        else:
            if field_value is None and f.required and f.default is None:
                raise BluePrintException(msg='Please specify value for field %s' % f.name)

            if f.data_type == 'string':
                assert isinstance(field_value, str)
            elif f.data_type == 'int':
                assert isinstance(field_value, int)
            elif f.data_type == 'float':
                assert isinstance(field_value, float)
            elif f.data_type == 'boolean':
                assert isinstance(field_value, bool)
            else:
                assert False, 'No such data type <%s>' % f.data_type
        return field_value

    def _serialize_map_field(self, f: Field):
        print(self.__class__.__dict__)
        assert f.container == 'map'
        assert issubclass(f.data_type, BluePrint)
        group_by: typing.List[str] = f.container_config.get('group_by')
        pass

    def _serialize_list_field(self, f: Field):
        print(self.__class__.__dict__)
        assert f.container == 'list'
        assert issubclass(f.data_type, BluePrint)

    def _serialize(self, validate=True) -> dict:
        """From object to dictionary"""
        return_data: dict = {}

        class_dict = self.__class__.__dict__
        for key in class_dict:
            value_obj = class_dict[key]
            if isinstance(value_obj, Field):
                if validate:
                    value = self.validate_field(value_obj)
                else:
                    value = getattr(self, key)
                return_data.update({key: value})

        return return_data

    def _deserialize(self, data: dict) -> typing.NoReturn:
        assert 'instance_id' in data
        class_dict = self.__class__.__dict__
        for key in class_dict:
            value_obj = class_dict[key]
            if isinstance(value_obj, Field):
                if type(value_obj.data_type) is BluePrintMeta:
                    # Only support storing Blueprints in container (map or list)
                    assert value_obj.container in Field.CONTAINERS
                    if value_obj.container == 'map':
                        pass
                    elif value_obj.container == 'list':
                        pass
                else:
                    pass

    def _der_simple(self, f: Field, value: typing.Any) -> BluePrintMeta:
        assert not f.container
        assert not f.container_config
        v = None

        if f.data_type == 'string':
            v = str(value)
        elif f.data_type == 'int':
            v = int(value)
        elif f.data_type == 'float':
            v = float(value)
        elif f.data_type == 'boolean':
            v = bool(value)

        setattr(self, f.name, v)
        return self

    def _der_map(self, f: Field, value: typing.Any) -> BluePrintMeta:
        assert issubclass(f.data_type, BluePrint)
        assert f.container == 'map'
        assert 'group_by' in f.container_config
        group_by: typing.List[str] = f.container_config['group_by']



