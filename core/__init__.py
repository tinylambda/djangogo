import threading
from collections import OrderedDict


class ProcessLevelRegistry:
    DEFAULT_DOMAIN = 'DEFAULT_DOMAIN'
    REGISTRY_LOCK = threading.RLock()
    REGISTRY = OrderedDict()

    @classmethod
    def register(cls, key, value, domain=DEFAULT_DOMAIN):
        with cls.REGISTRY_LOCK:
            if domain not in cls.REGISTRY:
                cls.REGISTRY[domain] = OrderedDict()
            cls.REGISTRY[domain].update({
                key: value
            })

    @classmethod
    def unregister(cls, key, domain=DEFAULT_DOMAIN):
        with cls.REGISTRY_LOCK:
            domain_registry = cls.REGISTRY.get(domain, {})
            try:
                domain_registry.pop(key)
            except KeyError:
                pass

    @classmethod
    def get(cls, key, domain=DEFAULT_DOMAIN):
        domain_registry = cls.REGISTRY.get(domain, {})
        value = domain_registry.get(key, None)
        return value

    @classmethod
    def get_domain_registry(cls, domain):
        return cls.REGISTRY.get(domain, {})

