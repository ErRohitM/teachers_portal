import django_filters
from .models import Student
import django_filters

class StudentFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    subject = django_filters.CharFilter(field_name='subject', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['name', 'subject']

