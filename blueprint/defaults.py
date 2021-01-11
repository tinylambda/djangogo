import json

DUMP_KWARGS = {
    "indent": " " * 4
}

CONFIG_DEFAULT = {
}
CONFIG_DEFAULT = json.dumps(
    CONFIG_DEFAULT, **DUMP_KWARGS
)

