from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse_lazy
from .models import Produit
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.core.mail import EmailMessage
from .form import AddForm, SaleForm
from .models import Produit,Vente,Categorie
from Application1.filters import ProductFilter
from django.views.generic import UpdateView
from django.http import JsonResponse
from django.db.models import F


00# Create your views here.
@login_required(login_url='logine')
def accueil(request):
 return render(request,"herite_page.html")  

# def formulaire(request):
#     return render(request, "formulaire.html")   
   
#insertion de nos produits
def insertproduit(request):
    form = AddForm()
    if request.method == 'POST':
        form = AddForm(request.POST)
        if form.is_valid():
            produit = form.save()
            added_quantity = int(request.POST['quantite_obtenue'])
            produit.quantite_total += added_quantity
            produit.save()
            return redirect('create')
            
    return render(request, "formulaire.html", {'form':form})

# Reçu des clients
def receipt(request): 
    sales = Vente.objects.all().order_by('-id')
    return render(request, 
    'Reçu.html', 
    {'sales': sales,
    })
# Détails su reçu
def receipt_detail(request, receipt_id):
    receipt = Vente.objects.get(id = receipt_id)
    return render(request, 'detail_reçu.html', {'receipt': receipt})

# Détails des produits
def product_detail(request, product_id):
    product = Produit.objects.get(id=product_id)
    
    if product.nom_article:
        return render(request, 'Detail_produit.html', {'product': product})
    else:
        return render(request, 'error.html', {'message': 'Article non trouvé'})

# les articles
def ajouter_vente(request, article_id):
    if request.method == 'POST':
        form = SaleForm(request.POST)
        if form.is_valid():
            vente = form.save(commit=False)
            produit = get_object_or_404(Produit, id=article_id)
            
            if produit.quantite_total >= vente.quantite:
                vente.article = produit
                vente.montant_obtenu = vente.get_total()
                vente.save()
                Produit.objects.filter(id=article_id).update(quantite_total=F('quantite_total') - vente.quantite)
                return redirect('receipt')
            else:
                form.add_error('quantite', 'Quantité insuffisante en stock.')
    else:
        form = SaleForm()
    return render(request, 'ajouter_vente.html', {'form': form})





# Connexion au compte
def connex(request):

    if request.method == "POST":
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)

        user = User.objects.filter(email=email).first()
        if user:
            auth_user = authenticate(username=user.username, password=password)
            if auth_user:
                login(request, auth_user)
                return redirect('home')
            else:
                print("mot de pass incorrecte")
        else:
            print("User does not exist")

    return render(request, 'authentification/connexion.html',)

# Mot de passe oublié
def forgot_password(request):
    error = False
    success = False
    message = ""
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            print("processing forgot password")
            html = """
                <p> Hello, merci de cliquer pour modifier votre email </p>
            """

            msg = EmailMessage(
                "Modification de mot de pass!",
                html,
                "soroib0879@gmail.com",
                ["soro4827@gmail.com"],
            )

            msg.content_subtype = 'html'
            msg.send()
            
            message = "processing forgot password"
            success = True
        else:
            print("user does not exist")
            error = True
            message = "user does not exist"
    
    context = {
        'success': success,
        'error':error,
        'message':message
    }
    return render(request, "Authentification/password_forget.html", context)

# Création de compte
def sing_up(request):
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        repassword = request.POST.get('repassword', None)
        # Email
        try:
            validate_email(email)
        except:
            error = True
            message = "Enter un email valide svp!"
        # password
        if error == False:
            if password != repassword:
                error = True
                message = "Les deux mot de passe ne correspondent pas!"
        # Exist
        user = User.objects.filter(Q(email=email) | Q(username=name)).first()
        if user:
            error = True
            message = f"Un utilisateur avec email {email} ou le nom d'utilisateur {name} exist déjà'!"
        
        # register
        if error == False:
            user = User(
                username = name,
                email = email,
            )
            user.save()

            user.password = password
            user.set_password(user.password)
            user.save()

            return redirect('logine')

            #print("=="*5, " NEW POST: ",name,email, password, repassword, "=="*5)

    context = {
        'error':error,
        'message':message
    }
    return render(request, 'Authentification/creation.html', context)

# Déconnexion du compte
def deconnexion(request):
    logout(request)
    return redirect('logine')

# Toutes les ventes éffectués
def all_sales(request):
    sales = Vente.objects.all()
    total  = sum([items.montant_obtenue for items in sales])
    change = sum([items.get_change() for items in sales])
    net = total - change
    return render(request, 'All_sales.html',
     {
     'sales': sales, 
     'total': total,
     'change': change, 
     'net': net,
      })

# Article en stock
def index(request):
    products = Produit.objects.all().order_by('-id')
    product_filters = ProductFilter(request.GET, queryset = products)
    products = product_filters.qs

    return render(request, 'stock_produit.html', {
        'products': products, 'product_filters': product_filters,
    })

# modification
# def Update(request, id):
#     if request.method == "POST":
#         categorie = request.POST.get('nom_categorie')  # Récupérer l'ID de la catégorie depuis le formulaire
#         article = request.POST.get('nom_article')
#         quantite = request.POST.get('quantite_total')
#         prix = request.POST.get('prix_unitaire')
        
#         # Récupérer l'instance de Categorie correspondante à l'ID
        
        
#         product = Produit.objects.get(id=id)  # Récupérer le produit existant
#         product.nom_categorie = nom_categorie  # Assigner l'instance de Categorie à l'attribut 'nom_categorie'
#         product.nom_article = article
#         product.quantite_total = quantite
#         product.prix_unitaire = prix
#         product.save()
#         return redirect('home')
    
#     product = Produit.objects.filter(id=id)
#     context = {'products': product}
    
#     return render(request, 'modif.html', context)

class Modification_Donnees(UpdateView):
    model = Produit
    form_class = AddForm
    template_name = "modif.html"
    success_url = reverse_lazy('index')


def accueil1(request):
    return render(request, 'accueil.html')    

def ajax_home_data(request):
    # Récupérer les dernières ventes (par exemple, les 5 dernières)
    latest_sales = Vente.objects.all().order_by('-id')[:5]
    sales_data = []
    for sale in latest_sales:
        # Formatage des données des ventes selon vos besoins
        sale_data = {
            'id': sale.id,
            'montant_obtenue': sale.montant_obtenue,
            # Autres champs pertinents
        }
        sales_data.append(sale_data)

    # Récupérer les produits en stock (par exemple, les 10 premiers)
    products_in_stock = Produit.objects.filter(quantite_total__gt=0)[:10]
    stock_data = []
    for product in products_in_stock:
        # Formatage des données des produits selon vos besoins
        product_data = {
            'id': product.id,
            'nom_article': product.nom_article,
            'quantite_total': product.quantite_total,
            # Autres champs pertinents
        }
        stock_data.append(product_data)

    # Créer un dictionnaire contenant les données mises à jour
    data = {
        'latest_sales': sales_data,
        'products_in_stock': stock_data,
    }

    # Renvoyer les données sous forme de réponse JSON
    return JsonResponse(data)

def supprimer_produit(request, produit_id):
    produit = Produit.objects.get(id=produit_id)
    produit.delete()
    return redirect('index')
    

