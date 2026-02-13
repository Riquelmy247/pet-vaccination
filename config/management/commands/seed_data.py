from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from pets.models import Pet
from vaccines.models import Vaccine
from vaccinations.models import Vaccination


class Command(BaseCommand):
    help = "Seed database with initial data for development and testing."

    def handle(self, *args, **options):
        User = get_user_model()

        if User.objects.exists():
            self.stdout.write(self.style.WARNING("Data already exists, skipping seeding."))
            return

        # Create users
        owner1 = User.objects.create_user(
            username="owner1@example.com",
            email="owner1@example.com",
            full_name="Owner One",
            phone_number="+1-555-0001",
            password="Passw0rd!",
        )
        owner2 = User.objects.create_user(
            username="owner2@example.com",
            email="owner2@example.com",
            full_name="Owner Two",
            phone_number="+1-555-0002",
            password="Passw0rd!",
        )

        # Create pets
        pet1 = Pet.objects.create(
            name="Rex",
            species="dog",
            breed="Labrador",
            birth_date=date.today() - timedelta(days=365),
            weight=30.5,
            owner=owner1,
        )
        pet2 = Pet.objects.create(
            name="Mia",
            species="cat",
            breed="Siamese",
            birth_date=date.today() - timedelta(days=200),
            weight=4.2,
            owner=owner2,
        )

        # Create vaccines
        rabies = Vaccine.objects.create(
            name="Rabies",
            manufacturer="VetPharma",
            description="Rabies vaccine for dogs and cats.",
            periodicity_days=365,
        )
        distemper = Vaccine.objects.create(
            name="Distemper",
            manufacturer="AnimalHealth",
            description="Canine distemper vaccine.",
            periodicity_days=365,
        )

        # Create vaccinations
        today = date.today()
        Vaccination.objects.create(
            pet=pet1,
            vaccine=rabies,
            application_date=today - timedelta(days=30),
            next_due_date=today + timedelta(days=335),
            notes="First rabies dose.",
            veterinarian_name="Dr. Smith",
        )
        Vaccination.objects.create(
            pet=pet2,
            vaccine=distemper,
            application_date=today - timedelta(days=10),
            next_due_date=today + timedelta(days=355),
            notes="Annual distemper vaccine.",
            veterinarian_name="Dr. Johnson",
        )

        self.stdout.write(self.style.SUCCESS("Seed data created successfully."))

