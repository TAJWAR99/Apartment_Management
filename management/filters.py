import django_filters
from .models import Owner

class OwnerFilter(django_filters.FilterSet):
    class Meta:
        model = Owner
        fields = '__all__'
        exclude = ['phone','nid','district','zipcode','thana','email','address']

class BillFilter(django_filters.FilterSet):
    class Meta:
        model = Owner
        fields = '__all__'
        exclude = ['phone','nid','district','zipcode','thana','email','address','name']