from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.utils import timezone
from datetime import date
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Deleting old data...')
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()
        User.objects.all().delete()
        Team.objects.all().delete()

        self.stdout.write('Creating teams...')
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        self.stdout.write('Creating users...')
        tony = User.objects.create(name='Tony Stark', email='tony@marvel.com', team=marvel)
        steve = User.objects.create(name='Steve Rogers', email='steve@marvel.com', team=marvel)
        bruce = User.objects.create(name='Bruce Wayne', email='bruce@dc.com', team=dc)
        clark = User.objects.create(name='Clark Kent', email='clark@dc.com', team=dc)

        self.stdout.write('Creating activities...')
        Activity.objects.create(user=tony, type='Running', duration=30, date=date.today())
        Activity.objects.create(user=steve, type='Cycling', duration=45, date=date.today())
        Activity.objects.create(user=bruce, type='Swimming', duration=60, date=date.today())
        Activity.objects.create(user=clark, type='Yoga', duration=20, date=date.today())

        self.stdout.write('Creating workouts...')
        w1 = Workout.objects.create(name='Super Strength', description='Strength workout for heroes')
        w2 = Workout.objects.create(name='Flight Training', description='Aerobic workout for flyers')
        w1.suggested_for.add(tony, bruce)
        w2.suggested_for.add(steve, clark)

        self.stdout.write('Creating leaderboard...')
        Leaderboard.objects.create(team=marvel, points=150)
        Leaderboard.objects.create(team=dc, points=120)

        self.stdout.write('Ensuring unique index on email field in users collection...')
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        db.users.create_index([('email', 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
