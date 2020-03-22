
from django.core.management.base import BaseCommand, CommandError





class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('-с', '--country', type=int)

    def handle(self, *args, **options):
        if options['country'] == 'canada':
            get_locations(country=)
        elif options['location'] == 'all':
            main_parse(search=options['search'], page=options['start'], quantity=options['quantity'])
