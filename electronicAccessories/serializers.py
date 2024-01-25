from rest_framework import serializers
from .models import Electronic, Supplier

class ElectronicSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Electronic
        fields = ['title', 'description', 'price', 'exist', 'supplier']

