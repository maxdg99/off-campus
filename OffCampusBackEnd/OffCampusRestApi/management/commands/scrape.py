from django.core.management.base import BaseCommand, CommandError
from scrape import scrape

class Command(BaseCommand):
    help = 'Scrape using the specified scraper classes'

    def add_arguments(self, parser):
        pass
        parser.add_argument('class_name', nargs='*', type=str, help="One or more python class names to scrape")

    def handle(self, *args, **options):
        class_names = options["class_name"]
        if len(class_names) == 0:
            class_names = None
        print("Scraping for classes: "+str(class_names))
        scrape(class_names)
        self.stdout.write(self.style.SUCCESS('Successfully scraped'))
