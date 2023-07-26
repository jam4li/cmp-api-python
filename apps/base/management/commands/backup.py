import os
import subprocess
import gzip
from pathlib import Path
from datetime import datetime
from django.conf import settings
from django.core.management.base import BaseCommand

from utils.mysqldump import execute_mysqldump


class Command(BaseCommand):
    help = 'Execute mysqldump to create a database backup.'

    def handle(self, *args, **options):
        message = execute_mysqldump()

        if message[1]:
            self.stdout.write(
                self.style.SUCCESS(
                    message[0]
                )
            )

        else:
            self.stdout.write(
                self.style.ERROR(
                    message[0]
                )
            )
