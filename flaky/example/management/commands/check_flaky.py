import logging
import os

from django.core.management.base import BaseCommand

from check.analyze import find_flaky_from_file

logger = logging.getLogger()


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to look for tests')

    def handle(self, *args, **options):
        path = options['path']

        for directory_name, _, files in os.walk(path):
            for file in files:
                if file.startswith('test_') and file.endswith('.py'):
                    full_path = os.path.join(directory_name, file)
                    try:
                        find_flaky_from_file(full_path)
                    except SyntaxError:
                        logger.warning('Skiping {}. Invalid syntax'.format(full_path))
                    except Exception:
                        logger.error('Failed processing {}'.format(full_path))
                        raise

