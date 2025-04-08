from django import forms
from .models import Guide
class GuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields = '__all__'

    def clean_latitude(self):
        latitude = self.cleaned_data.get('latitude')
        if latitude and (latitude < -90 or latitude > 90):
            raise forms.ValidationError("Latitude must be between -90 and 90.")
        return latitude

    def clean_longitude(self):
        longitude = self.cleaned_data.get('longitude')
        if longitude and (longitude < -180 or longitude > 180):
            raise forms.ValidationError("Longitude must be between -180 and 180.")
        return longitude
