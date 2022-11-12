import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treeMapperAPI.settings")
import django
django.setup()

from mappingAPI import models

myParks = [{'name':'Elizabeth Park','lat':'48.76000','lng':'-122.490773','zoom':18},
           {'name':'Memorial Park', 'lat':'48.76747','lng':'-122.462833','zoom':16},
           {'name':'Broadway Park','lat':'48.765189','lng':'-122.476687','zoom':17},
           {'name':'Boulevard Park','lat':'48.73209','lng':'-122.5021313','zoom':17}]

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