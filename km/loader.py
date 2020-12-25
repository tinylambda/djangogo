import typing

from .models import Concept
from .models import Attr


class KMLoader:
    def __init__(self):
        self.concepts = {}

    def load(self):
        self.concepts.clear()
        concept_db_objects: typing.List[Concept] = Concept.objects.all()
        for concept_db_object in concept_db_objects:
            concept_cls = self._load(concept_db_object.name)
            self.concepts.update({
                concept_cls.__name__: concept_cls
            })

    def _load(self, concept_name: str):
        concept = Concept.objects.get(name=concept_name)
        name = concept.name
        name_readable = concept.name_readable
        is_a: Concept = concept.is_a

        if is_a is None:
            concept_cls = type(name, (), {
                'name_readable': name_readable,
                'attrs': {},
            })
            return concept_cls
        else:
            parent_cls = self._load(is_a.name)
            concept_cls = type(name, (parent_cls, ), {
                'name_readable': name_readable,
                'attrs': {}
            })
            return concept_cls

    def _load_attr(self, attr: Attr):
        pass

