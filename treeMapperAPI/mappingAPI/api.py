from django.http import JsonResponse, HttpResponse

from mappingAPI.models import *
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def genera(request):
    if request.method == 'GET':
        genera = TreeSpecies.objects.filter().values("genus").distinct()
        myGenera = [] 
        for i in genera:
            myGenera.append(i['genus'])
        return JsonResponse(myGenera,safe=False)
