import json
import pprint
import openpyxl

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from rule.models import ConfigRule


class Command(BaseCommand):
    help = 'Load character configurations'

    DUMP_KWARGS = {
        "indent": " " * 4
    }

    def add_arguments(self, parser):
        parser.add_argument('xsl', nargs='?', type=str, help='configuration file (xsl)')

    def handle(self, *args, **options):
        conf_file = options['xsl']
        if not conf_file:
            raise CommandError(f"Please specify configuration file")
        wb = openpyxl.load_workbook(conf_file, data_only=True)
        sheet = wb.get_sheet_by_name('character_lv')
        input_keys = ['character.attr.level', 'character.config.quality']
        input_keys = json.dumps(input_keys, **self.DUMP_KWARGS)
        output_keys = ['character.cond.level_up_exp', 'character.cond.attr_addon']
        output_keys = json.dumps(output_keys, **self.DUMP_KWARGS)
        rules = []

        raw_configs = []
        i = 0
        for row in sheet:
            i += 1
            if i <= 2:
                continue
            if i == 3:
                headers = [c.value for c in row]
                continue

            values = [c.value for c in row]
            item_item = dict(zip(headers, values))
            raw_configs.append(item_item)

        new_configs = []
        for raw_config in raw_configs:
            new_config = {
                'character.state.level': raw_config['level'],
                'character.config.quality': 2
            }
            new_config.update({
                'character.cond.level_up_exp': raw_config['normal_need_exp'],
                'character.cond.attr_addon': raw_config['normal_extra_add'],
            })
            new_configs.append(new_config)

            new_config = {
                'character.state.level': raw_config['level'],
                'character.config.quality': 3
            }
            new_config.update({
                'character.cond.level_up_exp': raw_config['rare_need_exp'],
                'character.cond.attr_addon': raw_config['rare_extra_add'],
            })
            new_configs.append(new_config)

            new_config = {
                'character.state.level': raw_config['level'],
                'character.config.quality': 4
            }
            new_config.update({
                'character.cond.level_up_exp': raw_config['epick_need_exp'],
                'character.cond.attr_addon': raw_config['epick_extra_add'],
            })
            new_configs.append(new_config)

            new_config = {
                'character.state.level': raw_config['level'],
                'character.config.quality': 5
            }
            new_config.update({
                'character.cond.level_up_exp': raw_config['legend_need_exp'],
                'character.cond.attr_addon': raw_config['legend_extra_add'],
            })
            new_configs.append(new_config)

        pprint.pprint(new_configs)

