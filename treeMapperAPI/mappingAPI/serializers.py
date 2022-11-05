from rest_framework import serializers
from mappingAPI.models import * 


class SpeciesSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreeSpecies
        fields = '__all__'