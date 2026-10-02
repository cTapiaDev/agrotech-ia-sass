from rest_framework import serializers
from .models import Crop, FarmField

class CropSerializer(serializers.ModelSerializer):
    farm_field_id = serializers.PrimaryKeyRelatedField(
        queryset=FarmField.objects.all(),
        source='farm_field',
        write_only=True
    )

    class Meta:
        model = Crop
        fields = [
            'id', 'name', 'crop_type', 'sowing_date', 
            'harvest_date', 'is_active', 'farm_field_id',
            'farm_field'
        ]

        read_only_fields = ['farm_field']