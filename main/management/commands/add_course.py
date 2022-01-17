from django.core.management.base import BaseCommand
from main.models import Course

class Command(BaseCommand):
    help = 'Create Dummy Box locations'


    def handle(self, *args, **options):
        
        courses = [
            {
            'title':"Backend with Django"},
            {
            'title':"Data science with Python"},
            {
            'title':"Frontend Web Development"},
            {
            'title':"Product Design (UI/UX)"},
            ]
        a = []
        for course in courses:
            a.append(Course(**course))
            
        Course.objects.bulk_create(a)

        self.stdout.write(self.style.SUCCESS("Successfully added %s courses" %len(a)))