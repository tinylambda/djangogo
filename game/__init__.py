class Game:
    """
    A game is a collection of concepts and their relationships.
    A concept is a collection of related attributes.
    A concept prototype is a initialized state of a concept.
    A concept config is slowly (or never) changing attributes set.
    A concept state is a rapid changing attributes set (usually initialized as prototype)
    A rule is a rule how a set of attributes affect other attributes.
    A concept instance must hold a instance id to identify specific instance.
    Instance id can be generated based on attributes of concept instances.
    """
    def __init__(self):
        self.game_context = {}




