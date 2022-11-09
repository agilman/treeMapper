import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treeMapperAPI.settings")
import django
django.setup()

from mappingAPI import models


myParks = [{'name':'Elizabeth','lat':'48.76000','lng':'-122.490773','zoom':18}]
print("Adding parks:")
for i in myParks:
    print(i)
    newPark = models.Parks(name=i['name'],lat=i['lat'],lng=i['lng'],zoom=i['zoom'])
    newPark.save()


print("\nAdding Trees:")

trees = [{'genus':'Acer','species':'rubrum','commonName':'Red Maple','wiki':'https://en.wikipedia.org/wiki/Acer_rubrum'},
         {'genus':'Acer','species':'platanoides','commonName':'Norway Maple','wiki':'https://en.wikipedia.org/wiki/Acer_platanoides'},
         {'genus':'Acer','species':'saccharum','commonName':'Sugar Maple','wiki':'https://en.wikipedia.org/wiki/Acer_saccharum'},
         {'genus':'Arbutus','species':'menziesii','commonName':'Madrone','wiki':'https://en.wikipedia.org/wiki/Arbutus_menziesii'},
]
for i in trees:
    print(i["commonName"])
    newTree = models.TreeSpecies(genus=i['genus'], species=i['species'], commonName=i['commonName'], wiki=i['wiki'])
    newTree.save()