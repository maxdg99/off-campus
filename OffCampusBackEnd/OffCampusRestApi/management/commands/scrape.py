from django.core.management.base import BaseCommand, CommandError
from scrape import scrape

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        pass
        #parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        scrape()
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))
