from django.core.management.base import BaseCommand
from django.utils import timezone
from agronomy.models import CustomUser, FarmField, Crop
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Poblar la base de datos con registros para pruebas'

    def handle(self, *args, **kwargs):
        self.stdout.write('Iniciando poblado masivo de datos...')

        self.stdout.write('Generando usuarios...')
        users_to_create = []
        for i in range(1, 51):
            username = f'producer_{i}'
            if not CustomUser.objects.filter(username=username).exists():
                user = CustomUser(
                    username=username,
                    email=f'producer_{i}@agrotech.cl',
                    role=CustomUser.RoleChoices.PRODUCER
                )
                user.set_password('password123')
                users_to_create.append(user)

        CustomUser.objects.bulk_create(users_to_create, batch_size=100)
        producers = list(CustomUser.objects.filter(role=CustomUser.RoleChoices.PRODUCER))

        self.stdout.write('Generando campos agrícolas...')
        field_prefixes = ['Fundo', 'Parcela', 'Hacienda', 'Finca', 'Valle', 'Rancho', 'Viña']
        field_names = ['El Maitén', 'Los Aromos', 'La Esperanza', 'San Pedro', 'El Roble', 'Santa María', 'Las Acacias']

        fields_to_create = []
        for i in range(500):
            name = f"{random.choice(field_prefixes)} {random.choice(field_names)} #{i + 1}"
            fields_to_create.append(FarmField(
                owner=random.choice(producers),
                name=name,
                location_lat=round(random.uniform(-36.5, -33.0), 6),
                location_lng=round(random.uniform(-72.0, -70.0), 6),
                total_area_hectares=round(random.uniform(5.0, 300.0), 2)
            ))

        FarmField.objects.bulk_create(fields_to_create, batch_size=200)
        all_fields = list(FarmField.objects.all())

        self.stdout.write('Generando cultivos...')
        crop_catalog = [
            ('Trigo Panin', Crop.CropTypeChoices.CEREAL),
            ('Maíz Dulce', Crop.CropTypeChoices.CEREAL),
            ('Avena Negra', Crop.CropTypeChoices.CEREAL),
            ('Manzana Royal Gala', Crop.CropTypeChoices.FRUIT),
            ('Cereza Lapins', Crop.CropTypeChoices.FRUIT),
            ('Uva Cabernet', Crop.CropTypeChoices.FRUIT),
            ('Palto Hass', Crop.CropTypeChoices.FRUIT),
            ('Tomate Limachino', Crop.CropTypeChoices.VEGETABLE),
            ('Cebolla Morada', Crop.CropTypeChoices.VEGETABLE),
            ('Lechuga Costina', Crop.CropTypeChoices.VEGETABLE),
        ]

        today = timezone.now().date()
        crops_to_create = []

        for i in range(2500):
            crop_name, crop_type = random.choice(crop_catalog)
            sowing = today - timedelta(days=random.randint(10, 180))
            harvest = sowing + timedelta(days=random.randint(90, 240))

            crops_to_create.append(Crop(
                farm_field=random.choice(all_fields),
                name=f"{crop_name} Lote-{i + 1}",
                crop_type=crop_type,
                sowing_date=sowing,
                harvest_date=harvest
            ))

        Crop.objects.bulk_create(crops_to_create, batch_size=500)

        self.stdout.write(self.style.SUCCESS(
            'Datos inyectados con éxito!'
        ))