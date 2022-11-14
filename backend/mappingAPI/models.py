from django.db import models

class TreeSpecies(models.Model):
    genus = models.CharField(max_length=32)
    species = models.CharField(max_length=32)
    commonName = models.CharField(max_length=64)
    wiki = models.CharField(max_length=128)

class Parks(models.Model):
    name = models.CharField(max_length=32)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    zoom = models.IntegerField()
    
class Trees(models.Model):
    species = models.ForeignKey(TreeSpecies,on_delete=models.DO_NOTHING)
    park = models.ForeignKey(Parks,on_delete=models.DO_NOTHING)
    lat = models.DecimalField(max_digits=9, decimal_places=6)
    lng = models.DecimalField(max_digits=9, decimal_places=6)
    size = models.IntegerField()   

class TreePhotos(models.Model):
    tree = models.ForeignKey(Trees,on_delete=models.CASCADE)
    ts = models.DateTimeField()

class TreeNotes(models.Model):
    tree = models.ForeignKey(Trees,on_delete=models.CASCADE)
    ts = models.DateTimeField()
    text = models.CharField(max_length=128)