import typing
import time
import random
import string

from km.concepts import Concepts


class GameElement:
    Concepts.load()
    CONCEPT_NAME = None

    def __init__(self):
        self.buffer_info: dict = {}
        self.instance_id: str = None
        self.create_ts: int = None
        self.instance_id_template = None

    def get_prototype(self):
        pass

    def serialize(self):
        pass

    def deserialize(self, data: typing.Dict):
        pass

    def get_config(self, config_id: str):
        pass


class Character(GameElement):
    CONCEPT_NAME = 'character'

    def __init__(self, **kwargs) -> typing.NoReturn:
        super(Character, self).__init__()
        self.config_id: str = kwargs.get('config_id')
        self.level: int = 1
        self.star: int = 1
        self.exp: int = 0
        self.instance_id_template = '{config_id}_{create_ts}_{rand_str}'

    def serialize(self) -> typing.Dict:
        """
        Serialize existing instance or newly created instance to dictionary
        """
        if not self.config_id:
            raise RuntimeError(f'Character config_id should not be None')

        data: typing.Dict = {
            'config_id': self.config_id,
            'level': self.level,
            'exp': self.exp,
            'star': self.star,
        }

        if not self.instance_id:
            # Newly created instance
            self.create_ts = int(time.time())
            data.update({
                'create_ts': self.create_ts,
            })

            rand_str = ''.join(
                random.sample(string.ascii_letters + string.digits, 6)
            )

            self.instance_id = self.instance_id_template.format(rand_str=rand_str, **data)

        data.update({
            'instance_id': self.instance_id,
        })

        return data

    def deserialize(self, data: typing.Dict):
        """
        Deserialize from existing instance data
        """
        instance_id: str = data.get('instance_id')
        if instance_id is None:
            raise RuntimeError('Character instance_id should not be None')
        self.instance_id = instance_id
        self.level = data.get('level')
        self.star = data.get('star')
        self.exp = data.get('exp')
        self.config_id = data.get('config_id')
        self.create_ts = data.get('create_ts')

    def get_config(self) -> typing.Dict:
        concept_cls = Concepts.get_concept_cls(self.CONCEPT_NAME)
        config: dict = concept_cls.get_config(self.config_id)
        return config


class Role(GameElement):
    def __init__(self):
        super().__init__()
        self.server_id: str = None
        self.role_id: str = None
        self.strength = None
        self.characters: typing.List[Character] = []
        self.instance_id_template = '{server_id}_{role_id}'

    def serialize(self):
        pass

    def deserialize(self, data: typing.Dict):
        pass

    def get_prototype(self):
        pass

    def get_config(self, config_id: str):
        pass








