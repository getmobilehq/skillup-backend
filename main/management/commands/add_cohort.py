from django.core.management.base import BaseCommand
from main.models import Cohort

class Command(BaseCommand):
    help = 'Create Dummy Box locations'


    def handle(self, *args, **options):
        
        cohorts = [
            {
            'title':"January 2022"},
            {
            'title':"March 2022"},
            ]
        a = []
        for cohort in cohorts:
            a.append(Cohort(**cohort))
            
        Cohort.objects.bulk_create(a)

        self.stdout.write(self.style.SUCCESS("Successfully added %s cohorts" %len(a)))