from django.urls import path
from .views import *

urlpatterns = [
    path('', accueil,name="home"),
    path('receipt/', receipt, name='receipt'),
    path('receipt/<int:receipt_id>/', receipt_detail, name='receipt_detail'),
    path('product_detail/<int:product_id>/', product_detail, name='Produit'),
    path('vente/<int:article_id>/', ajouter_vente, name='ajouter_vente'),
    path('create/', insertproduit,name="create"),
    path('login', connex, name='logine'),
    path('forgot-password', forgot_password, name='forgot_password'), 
    path('register', sing_up, name='sing_up'), 
    path('logout', deconnexion, name='logout'), 
    path('all_sales/', all_sales, name = 'all_sales'),
    path('index/', index, name = "index"),
    # path('update/<str:id>',Update, name='update'),
    path('modifier/<int:pk>/',Modification_Donnees.as_view(), name ='modifier'), 
    path('Accueil', accueil1, name='accueil') ,
    path('ajax_home_data/', ajax_home_data, name='ajax_home_data'),
    path('produit/<int:produit_id>/supprimer/', supprimer_produit, name='supprimer_produit'),
]
