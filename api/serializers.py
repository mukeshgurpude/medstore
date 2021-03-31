from rest_framework import serializers
from medicines.models import Medicine, MedCat


class MedicineSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Medicine
        fields = ['name', 'price', 'slug', 'description', 'quantity', 'category', 'owner']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedCat
