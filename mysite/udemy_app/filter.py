from .models import Course
from django_filters.rest_framework import FilterSet


class CourseFilter(FilterSet):
    class Meta:
        model = Course
        fields = {
            'category': ['exact'],
            'sub_category': ['exact'],
            'price': ['gt', 'lt']
        }