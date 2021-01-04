import json
import openpyxl

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from state.models import State
from config.models import CommonConfig


class Command(BaseCommand):
    help = 'Load item configurations'

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
        sheet = wb.get_sheet_by_name('item')
        config = {}

        i = 0
        for row in sheet:
            i += 1
            if i <= 2:
                continue
            if i == 3:
                headers = [c.value for c in row]
                continue

            values = [c.value for c in row]
            config_item = dict(zip(headers, values))
            item_id = config_item.pop('item_id')
            config_item.update({
                'config_id': item_id
            })
            if None in config_item:
                config_item.pop(None)
            config[config_item['config_id']] = config_item

        state_item = State.objects.get(name='item')
        CommonConfig.objects.filter(config_for=state_item).delete()
        for config_id in config:
            if config_id is None:
                break

            config_body = config[config_id]
            config_body = json.dumps(
                config_body,
                ensure_ascii=False,
                **self.DUMP_KWARGS
            )
            common_config = CommonConfig.objects.create(
                config_for=state_item,
                config_id=config_id,
                config=config_body
            )

        self.stdout.write(self.style.SUCCESS("Done"))
