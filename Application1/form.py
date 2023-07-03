from django import forms
from .models import *

class AddForm(forms.ModelForm):
    class Meta:
        model = Produit
        fields = ['nom_categorie', 'nom_article', 'quantite_total', 'quantite_emise', 'quantite_obtenue', 'prix_unitaire']
        widgets = {
            'nom_article': forms.TextInput(attrs={'class': 'form-control'}),
            'quantite_total': forms.TextInput(attrs={'class': 'form-control'}),
            'quantite_emise': forms.TextInput(attrs={'class': 'form-control'}),
            'quantite_obtenue': forms.TextInput(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.TextInput(attrs={'class': 'form-control'}),
}

class SaleForm(forms.ModelForm):
    class Meta:
        model = Vente
        fields = ['quantite', 'montant_obtenue','prix_unitaire', 'delivre_A']
        widgets = {
            'quantite': forms.TextInput(attrs={'class': 'form-control'}),
            'montant_obtenue': forms.TextInput(attrs={'class': 'form-control'}),
            'delivre_A': forms.TextInput(attrs={'class': 'form-control'}),
            'prix_unitaire': forms.TextInput(attrs={'class': 'form-control'}),
            
}


