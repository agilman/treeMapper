from rest_framework import serializers
from mappingAPI.models import * 

class ParksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parks
        fields = '__all__'

class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeSpecies
        fields = '__all__'