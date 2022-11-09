from django.http import JsonResponse, HttpResponse

from mappingAPI.models import *
from django.views.decorators.csrf import csrf_exempt

from mappingAPI.serializers import *

@csrf_exempt
def parks(request):
    if request.method == 'GET':
        parks = Parks.objects.all()
        serializedParks = ParksSerializer(parks, many=True).data
        return JsonResponse(serializedParks, safe=False)

@csrf_exempt
def genera(request):
    if request.method == 'GET':
        genera = TreeSpecies.objects.filter().values("genus").distinct()
        myGenera = [] 
        for i in genera:
            myGenera.append(i['genus'])
        return JsonResponse(myGenera,safe=False)


@csrf_exempt
def species(request, genus):
    if request.method == 'GET':
        species = TreeSpecies.objects.all().filter(genus=genus)
        serializedSpecies = SpeciesSerializer(species, many=True).data
        return JsonResponse(serializedSpecies,safe=False)
