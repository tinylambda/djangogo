class Checker:
    @classmethod
    def load_rules(cls):
        pass

    @classmethod
    def check(cls, key, value, blueprint_context: dict):
        """
        Check if key can be set to value according to the newest rules
        """
        print(f'I am checking {key} = {value} with context {blueprint_context}')


Checker.load_rules()

