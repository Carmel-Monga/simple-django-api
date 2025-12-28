from django import forms
from .models import App

# Simple form used by the web frontend to add a new App.
# The widgets use Bootstrap classes so the default template renders
# a clean form without extra styling in the template itself.
class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = ['name', 'category', 'rating', 'reviews', 'size', 'installs', 'type', 'price', 'content_rating', 'genres', 'last_updated', 'current_version', 'android_version']
        # Add custom form controls so fields pick up Bootstrap styling.
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'reviews': forms.NumberInput(attrs={'class': 'form-control'}),
            'size': forms.TextInput(attrs={'class': 'form-control'}),
            'installs': forms.TextInput(attrs={'class': 'form-control'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.TextInput(attrs={'class': 'form-control'}),
            'content_rating': forms.TextInput(attrs={'class': 'form-control'}),
            'genres': forms.TextInput(attrs={'class': 'form-control'}),
            'last_updated': forms.TextInput(attrs={'class': 'form-control'}),
            'current_version': forms.TextInput(attrs={'class': 'form-control'}),
            'android_version': forms.TextInput(attrs={'class': 'form-control'}),
        }
    # Validation for the rating field. Ensure the submitted value is between 0 and 5.
    def clean_rating(self):
        r = self.cleaned_data.get('rating')
        if r is not None and (r < 0 or r > 5):
            raise forms.ValidationError('Rating must be between 0 and 5')
        return r
