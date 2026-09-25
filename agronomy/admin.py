from django.contrib import admin
from .models import CustomUser, FarmField, Crop, WeatherLog

admin.site.register(CustomUser)
admin.site.register(FarmField)
admin.site.register(Crop)
admin.site.register(WeatherLog)