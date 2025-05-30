from django.contrib.admin.views import autocomplete
from django import forms
from . models import Student

class StudentForm(forms.ModelForm):
    # created_by = forms.CharField(max_length=255, required=False)
    class Meta:
        model = Student
        fields = ['name', 'subject', 'marks']

class StudentSearchForm(forms.Form):
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search by name', 'class': 'form-control'}))
    subject = forms.CharField(required=False, widget=forms.TextInput(attrs={'placeholder': 'Search by subject', 'class': 'form-control'}))