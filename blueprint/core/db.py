class DB:
    """Simulate KV DB"""
    DATA = {}

    @classmethod
    def get(cls, k):
        return cls.DATA.get(k)

    @classmethod
    def set(cls, k, v):
        cls.DATA.update({k: v})
