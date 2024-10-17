# management/commands/create_auditoriums.py
from django.core.management.base import BaseCommand
from myapp.models import Theatre, Auditorium

class Command(BaseCommand):
    help = 'Create two auditoriums for each theatre'

    def handle(self, *args, **kwargs):
        theatres = Theatre.objects.all()
        for theatre in theatres:
            Auditorium.objects.get_or_create(theatre=theatre, name='Auditorium 1', capacity=100)  # Adjust capacity as needed
            Auditorium.objects.get_or_create(theatre=theatre, name='Auditorium 2', capacity=100)  # Adjust capacity as needed
        self.stdout.write(self.style.SUCCESS('Successfully created auditoriums for all theatres.'))