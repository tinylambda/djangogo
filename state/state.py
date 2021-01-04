import typing
import random
import string


class BaseState:
    STATE_ATTR_PREFIX = 'state__'

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
        Serialize existing instance or newly created instance to dictionary
        """
        pass

    def deserialize(self):
        pass



