import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treeMapperAPI.settings")
import django
django.setup()

from mappingAPI import models

myParks = [{'name':'Elizabeth Park','lat':'48.76000','lng':'-122.490773','zoom':18},
           {'name':'Memorial Park', 'lat':'48.76747','lng':'-122.462833','zoom':16},
           {'name':'Broadway Park','lat':'48.765189','lng':'-122.476687','zoom':17},
           {'name':'Laurel Park','lat':'48.7427511','lng':'-122.478471','zoom':18},
           {'name':'Boulevard Park','lat':'48.73209','lng':'-122.5021313','zoom':17}]
        

print("Adding parks:")
for i in myParks:
    print(i)
    newPark = models.Parks(name=i['name'],lat=i['lat'],lng=i['lng'],zoom=i['zoom'])
    newPark.save()


print("\nAdding Trees:")

trees = [{'genus':'Acer','species':'campestre','commonName':'Field Maple','wiki':'https://en.wikipedia.org/wiki/Acer_campestre'},
         {'genus':'Acer','species':'rubrum','commonName':'Red Maple','wiki':'https://en.wikipedia.org/wiki/Acer_rubrum'},
         {'genus':'Acer','species':'platanoides','commonName':'Norway Maple','wiki':'https://en.wikipedia.org/wiki/Acer_platanoides'},
         {'genus':'Acer','species':'saccharum','commonName':'Sugar Maple','wiki':'https://en.wikipedia.org/wiki/Acer_saccharum'},
         {'genus':'Acer','species':'macrophyllum','commonName':'Bigleaf Maple','wiki':'https://en.wikipedia.org/wiki/Acer_macrophyllum'},
         {'genus':'Arbutus','species':'menziesii','commonName':'Madrone','wiki':'https://en.wikipedia.org/wiki/Arbutus_menziesii'},
         {'genus':'Cedrus','species':'deodara','commonName':'Deodar Cedar','wiki':'https://en.wikipedia.org/wiki/Cedrus_deodara'},
         {'genus':'Cornus','species':'mas','commonName':'Cornelian Cherry','wiki':'https://en.wikipedia.org/wiki/Cornus_mas'},
         {'genus':'Cornus','species':'florida','commonName':'Flowering Dogwood','wiki':'https://en.wikipedia.org/wiki/Cornus_florida'},
         {'genus':'Fagus','species':'sylvatica','commonName':'European Beech','wiki':'https://en.wikipedia.org/wiki/Fagus_sylvatica'},
         {'genus':'Fraxinus','species':'americana','commonName':'White Ash','wiki':'https://en.wikipedia.org/wiki/Fraxinus_americana'},
         {'genus':'Ginkgo','species':'biloba','commonName':'Ginkgo','wiki':'https://en.wikipedia.org/wiki/Ginkgo_biloba'},
         {'genus':'Ilex','species':'aquifolium','commonName':'English Holly','wiki':'https://en.wikipedia.org/wiki/Ilex_aquifolium'},
         {'genus':'Picea','species':'orientalis','commonName':'Oriental Spruce','wiki':'https://en.wikipedia.org/wiki/Picea_orientalis'},
         {'genus':'Pinus','species':'contorta','commonName':'Shore Pine','wiki':'https://en.wikipedia.org/wiki/Pinus_contorta'},
         {'genus':'Pinus','species':'monticola','commonName':'Western White Pine','wiki':'https://en.wikipedia.org/wiki/Western_white_pine'},
         {'genus':'Quercus','species':'rubra','commonName':'Northern Red Oat','wiki':'https://en.wikipedia.org/wiki/Quercus_rubra'},
         {'genus':'Quercus','species':'robur','commonName':'English Oak','wiki':'https://en.wikipedia.org/wiki/Quercus_robur'},
         {'genus':'Quercus','species':'coccinea','commonName':'English Oak','wiki':'https://en.wikipedia.org/wiki/Quercus_coccinea'},
         {'genus':'Pseudotsuga','species':'menziesii','commonName':'Douglas Fir','wiki':'https://en.wikipedia.org/wiki/Douglas_fir'},
         {'genus':'Robinia','species':'pseudoacacia','commonName':'Black Locust','wiki':'https://en.wikipedia.org/wiki/Robinia_pseudoacacia'},
         {'genus':'Tsuga','species':'heterophylla','commonName':'Western Hemlock','wiki':'https://en.wikipedia.org/wiki/Tsuga_heterophylla'},
         {'genus':'Ulmus','species':'americana','commonName':'White Elm','wiki':'https://en.wikipedia.org/wiki/Ulmus_americana'},
         {'genus':'Ulmus','species':'minor','commonName':'Field Elm','wiki':'https://en.wikipedia.org/wiki/Ulmus_minor'}
]
for i in trees:
    print(i["commonName"])
    newTree = models.TreeSpecies(genus=i['genus'], species=i['species'], commonName=i['commonName'], wiki=i['wiki'])
    newTree.save()