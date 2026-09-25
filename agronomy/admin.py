from django.contrib import admin
from django.template.response import TemplateResponse
from django.conf import settings
from pymongo import MongoClient
from .models import CustomUser, FarmField, Crop, WeatherLog, MongoLogTracker

admin.site.register(CustomUser)
admin.site.register(FarmField)
admin.site.register(Crop)
# admin.site.register(WeatherLog)

@admin.register(MongoLogTracker)
class MongoLogTrackerAdmin(admin.ModelAdmin):
    def changelist_view(self, request, extra_context=None):
        client = MongoClient(settings.MONGODB_URI)
        db = client[settings.MONGODB_NAME]

        context = dict(
            self.admin_site.each_context(request),
            weather_logs=list(db.weather_logs.find().sort('created_at', -1).limit(50)),
            ai_logs=list(db.ai_logs.find().sort('created_at', -1).limit(50)),
            title="Registros Dual DB (MongoDB)"
        )

        return TemplateResponse(request, "admin/mongodb_changelist.html", context)