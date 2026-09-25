from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class RoleChoices(models.TextChoices):
        PRODUCER = 'PRODUCER', 'Productor'
        AGRONOMIST = 'AGRONOMIST', 'Agrónomo'

    role = models.CharField(
        max_length=15,
        choices=RoleChoices.choices,
        default=RoleChoices.PRODUCER,
        verbose_name='Rol del Usuario'
    )

    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"


class FarmField(models.Model):
    id = models.BigAutoField(primary_key=True)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fields', verbose_name='Propietario')
    name = models.CharField(max_length=100, verbose_name='Nombre del Campo')
    location_lat = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Latitud')
    location_lng = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Longitud')
    total_area_hectares = models.DecimalField(max_digits=7, decimal_places=2, verbose_name='Área Total (Hectáreas)')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    def __str__(self):
        return self.name

class Crop(models.Model):
    class CropTypeChoices(models.TextChoices):
        CEREAL = 'CEREAL', 'Cereal'
        FRUIT = 'FRUIT', 'Frutal'
        VEGETABLE = 'VEGETABLE', 'Vegetales'

    id = models.BigAutoField(primary_key=True)
    farm_field = models.ForeignKey(FarmField, on_delete=models.CASCADE, related_name='crops', verbose_name='Campo Asociado')
    name = models.CharField(max_length=100, verbose_name='Nombre del Cultivo')
    crop_type = models.CharField(max_length=20, choices=CropTypeChoices.choices, verbose_name='Tipo de Cultivo')
    sowing_date = models.DateField(verbose_name='Fecha de Siembra')
    harvest_date = models.DateField(null=True, blank=True, verbose_name='Fecha Estimada de Cosecha')
    is_active = models.BooleanField(default=True, verbose_name='Activo')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    def __str__(self):
        return f"{self.name} ({self.get_crop_type_display()})"


class WeatherLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    farm_field = models.ForeignKey(FarmField, on_delete=models.CASCADE, related_name='weather_logs')
    temperature = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Temperatura (°C)')
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Velocidad del Viento (km/h)')
    is_successful = models.BooleanField(default=True)
    error_message = models.TextField(null=True, blank=True)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Clima {self.farm_field.name} - {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"

class MongoLogTracker(models.Model):
    class Meta:
        managed = False
        verbose_name = "Auditoría NoSQL"
        verbose_name_plural = "Auditorías NoSQL"

# class Crop(models.Model):
#     name = models.CharField(max_length=100)
#     sowing_date = models.DateField()

#     def __str__(self):
#         return self.name