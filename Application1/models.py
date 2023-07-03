from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Categorie(models.Model):
    name = models.CharField(max_length = 50, null = True, blank = True)
    def __str__(self):
        return self.name


class Produit(models.Model):
    nom_categorie = models.ForeignKey(Categorie, on_delete = models.CASCADE,null = True, blank = True )
    nom_article = models.CharField(max_length = 50, null = True, blank = True)
    quantite_total = models.IntegerField(default = 0, null = True, blank = True)
    quantite_emise = models.IntegerField(default = 0, null = True, blank = True)
    quantite_obtenue = models.IntegerField(default = 0, null = True, blank = True)
    prix_unitaire = models.IntegerField(default = 0, null = True, blank = True)

    def __str__(self):
        return self.nom_article
    
    def is_low_quantity(self):
        return self.quantite_total < 10

  

class Vente(models.Model):
    article = models.ForeignKey(Produit, on_delete = models.CASCADE)
    quantite = models.IntegerField(default = 0, null = True, blank = True)
    montant_obtenue= models.IntegerField(default = 0, null = True, blank = True)
    delivre_A = models.CharField(max_length = 50, null = True, blank = True)
    prix_unitaire = models.IntegerField(default = 0, null = True, blank = True)

    def get_total(self):
        total = self.quantite * self.article.prix_unitaire
        return int(total)
    
    def get_change(self):
        change = self.get_total() - self.montant_obtenue
        return abs(int(change))

    
    def __str__(self):
        return self.article.nom_article
    


