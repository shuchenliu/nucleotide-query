from django.core.management import BaseCommand

from api.genome.reference import GenomeReference


class Command(BaseCommand):
    help = "Preload sequence data into memory and database"

    def handle(self, *args, **options):
        GenomeReference.prepare()