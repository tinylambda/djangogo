import json

DUMP_KWARGS = {
    "indent": " " * 4
}

ATTR_OPTIONS_DEFAULT = {
    'type': 'string',
    'required': True,
    'default': None,
    'container': None,
    'container_config': {},
}
ATTR_OPTIONS_DEFAULT = json.dumps(
    ATTR_OPTIONS_DEFAULT, **DUMP_KWARGS
)

