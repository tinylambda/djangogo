import os
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Manage the supervisord service"

    def add_arguments(self, parser):
        parser.add_argument("action", nargs="?", help="specify the action you want to run", type=str)

    @classmethod
    def prepare_configuration_files(cls):
        supervisord_conf_filename = getattr(settings, "SUPERVISORD_CONF_FILENAME", None)
        if supervisord_conf_filename is None:
            raise CommandError("settings.SUPERVISORD_CONF_FILENAME not specified")

        supervisord_log_root_path = getattr(settings, "SUPERVISORD_LOG_ROOT_PATH", None)
        if supervisord_log_root_path is None:
            raise CommandError("settings.SUPERVISORD_LOG_ROOT_PATH not specified")

        supervisord_conf_dirname = os.path.dirname(supervisord_conf_filename)
        if not os.path.exists(supervisord_conf_dirname):
            os.makedirs(supervisord_conf_dirname)

        if not os.path.exists(supervisord_log_root_path):
            os.makedirs(supervisord_log_root_path)

        with open(supervisord_conf_filename, 'w') as f:
            settings.SUPERVISORD_CONFIG.write(f)

    @classmethod
    def run_supervisorctl_cmd(cls, cmd_name):
        supervisord_conf_filename = getattr(settings, "SUPERVISORD_CONF_FILENAME", None)
        cmd = ["supervisorctl", "-c", supervisord_conf_filename, cmd_name]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            pass

    @classmethod
    def action_update_conf_file(cls, *args, **options):
        cls.prepare_configuration_files()

    @classmethod
    def action_start(cls, *args, **options):
        cls.prepare_configuration_files()
        supervisord_conf_filename = getattr(settings, "SUPERVISORD_CONF_FILENAME", None)
        cmd = ["supervisord", "-c", supervisord_conf_filename]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            pass

    @classmethod
    def action_stop(cls, *args, **options):
        cls.run_supervisorctl_cmd("shutdown")

    @classmethod
    def action_shell(cls, *args, **options):
        supervisord_conf_filename = getattr(settings, "SUPERVISORD_CONF_FILENAME", None)
        cmd = ["supervisorctl", "-c", supervisord_conf_filename]
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            pass

    @classmethod
    def action_status(cls, *args, **options):
        cls.run_supervisorctl_cmd("status")

    @classmethod
    def action_reload(cls, *args, **options):
        cls.run_supervisorctl_cmd("reload")

    def handle(self, *args, **options):
        supported_actions = [item.replace("action_", "") for item in dir(self) if item.startswith("action_")]
        action = options['action']
        if not action:
            raise CommandError(f"Please specify the action, supported actions: {','.join(supported_actions)}")
        action_method_name = f"action_{action}"

        try:
            getattr(self, action_method_name)(*args, **options)
        except AttributeError:
            raise CommandError(f"Unsupported action {action}, supported actions: {','.join(supported_actions)}")

        self.stdout.write(self.style.SUCCESS("Done"))
