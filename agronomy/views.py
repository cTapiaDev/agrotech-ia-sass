from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from .models import FarmField, Crop
from .mixins import ProducerRequiredMixin
from .tasks import sync_field_weather, analyze_crop_with_ai
from .forms import FarmFieldForm, CropForm

class FarmFieldListView(LoginRequiredMixin, ListView):
    model = FarmField
    template_name = 'agronomy/farmfield_list.html'
    context_object_name = 'farm_fields'

    def get_queryset(self):
        return FarmField.objects.filter(is_active=True).order_by('-created_at')

class CropListView(LoginRequiredMixin, ListView):
    model = Crop
    template_name = 'agronomy/crop_list.html'
    context_object_name = 'crops'

    def get_queryset(self):
        return Crop.objects.filter(is_active=True).select_related('farm_field').order_by('-created_at')

    

class FarmFieldCreateView(ProducerRequiredMixin, CreateView):
    model = FarmField
    template_name = 'agronomy/farmfield_form.html'
    form_class = FarmFieldForm
    success_url = reverse_lazy('farmfield_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        response = super().form_valid(form)
        sync_field_weather.delay(self.object.pk)
        return response

class FarmFieldUpdateView(ProducerRequiredMixin, UpdateView):
    model = FarmField
    template_name = 'agronomy/farmfield_form.html'
    form_class = FarmFieldForm
    success_url = reverse_lazy('farmfield_list')

class FarmFieldDeleteView(ProducerRequiredMixin, DeleteView):
    model = FarmField
    template_name = 'agronomy/farmfield_confirm_delete.html'
    success_url = reverse_lazy('farmfield_list')

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CropCreateView(ProducerRequiredMixin, CreateView):
    model = Crop
    template_name = 'agronomy/crop_from.html'
    form_class = CropForm
    success_url = reverse_lazy('crop_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        analyze_crop_with_ai.delay(self.object.pk)
        return response

class CropUpdateView(ProducerRequiredMixin, UpdateView):
    model = Crop
    template_name = 'agronomy/crop_from.html'
    form_class = CropForm
    success_url = reverse_lazy('crop_list')

class CropDeleteView(ProducerRequiredMixin, DeleteView):
    model = Crop
    template_name = 'agronomy/crop_confirm_delete.html'
    success_url = reverse_lazy('crop_list')

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())