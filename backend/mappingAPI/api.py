from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser

from mappingAPI.models import *
from django.views.decorators.csrf import csrf_exempt

from mappingAPI.serializers import *
import datetime
import pytz

@csrf_exempt
def parks(request):
    if request.method == 'GET':
        parks = Parks.objects.all()
        serializedParks = ParksSerializer(parks, many=True).data
        return JsonResponse(serializedParks, safe=False)

@csrf_exempt
def genera(request):
    if request.method == 'GET':
        genera = TreeSpecies.objects.filter().values("genus").distinct().order_by("genus")
        myGenera = [] 
        for i in genera:
            myGenera.append(i['genus'])
        return JsonResponse(myGenera,safe=False)


@csrf_exempt
def species(request, genus):
    if request.method == 'GET':
        species = TreeSpecies.objects.all().filter(genus=genus).order_by("species")
        serializedSpecies = SpeciesSerializer(species, many=True).data
        return JsonResponse(serializedSpecies,safe=False)

@csrf_exempt
def trees(request,parkId=None):
    if request.method == 'GET':
        data = Trees.objects.all()
        myTrees = TreesSerializer(data, many=True).data
        return JsonResponse(myTrees, safe=False)
    
    if request.method == 'POST':
        data = JSONParser().parse(request)
        parkId = data["park"]
        speciesId = data["species"]
        lat = data["lat"]
        lng = data["lng"]
        size = data["size"]

        park = Parks.objects.get(id=parkId)
        species = TreeSpecies.objects.get(id=speciesId)

        newTree = Trees.objects.create(park=park,species=species,lat=lat,lng=lng,size=size)
        serialized = TreesSerializer(newTree).data
        return JsonResponse(serialized,safe=False)

@csrf_exempt
def tree(request,treeId):
    if request.method =='DELETE':
        myTree = Trees.objects.get(id=treeId)
        myTree.delete()
        return JsonResponse(['OK'],safe=False)
        
@csrf_exempt
def notes(request,treeId=None):
    if request.method=='GET':
        data = TreeNotes.objects.filter(tree=treeId)
        myNotes = NotesSerializer(data, many=True).data
        return JsonResponse(myNotes, safe=False)
    if request.method=='POST':
        data = JSONParser().parse(request)
        treeId = data["tree"]
        text = data["text"]

        tzinfo = pytz.timezone('US/Pacific')
        now = datetime.datetime.now(tzinfo)

        tree = Trees.objects.get(id=treeId)

        newNote = TreeNotes.objects.create(tree=tree,ts=now,text=text)
        serialized = NotesSerializer(newNote).data
        return JsonResponse(serialized,safe=False)

