import typing
import json

from .models import ConfigRule


class RuleBase:
    def __init__(
            self,
            input_keys: typing.List[str],
            output_keys: typing.List[str],
            rules: typing.List[dict],
    ):
        self.input_keys: typing.List[str] = input_keys
        self.output_keys: typing.List[str] = output_keys
        self.rules: typing.List[dict] = rules


class Rules:
    @classmethod
    def __rule_name__(cls, name):
        return f'rule__{name}'

    @classmethod
    def load(cls):
        rule_db_objects: typing.List[ConfigRule] = ConfigRule.objects.all()
        for rule_db_object in rule_db_objects:
            cls._load_rule(rule_db_object)

    @classmethod
    def _load_rule(cls, rule_db_object: ConfigRule):
        input_keys = json.loads(rule_db_object.input_keys)
        output_keys = json.loads(rule_db_object.output_keys)
        rules = json.loads(rule_db_object.rules)
        rule_object = RuleBase(input_keys, output_keys, rules)

        for output_key in output_keys:
            rule_name = cls.__rule_name__(output_key)
            setattr(cls, rule_name, rule_object)

