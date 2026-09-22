from django import forms
from .models import FarmField, Crop

class TailwindFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full border-none p-3 outline-none bg-transparent text-slate-800'
            })

class FarmFieldForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = FarmField
        fields = ['name', 'location_lat', 'location_lng', 'total_area_hectares']

class CropForm(TailwindFormMixin, forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['farm_field', 'name', 'crop_type', 'sowing_date', 'harvest_date']
        widgets = {
            'sowing_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'harvest_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }