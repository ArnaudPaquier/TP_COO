# mysite/models.py
from django.db import models


class Ingredient(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom}"


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def cost(self):
        return self.prix


class Departement(models.Model):
    numero = models.IntegerField()
    prix_m2 = models.IntegerField()

    def __str__(self):
        return f"Département {self.numero}"

    def cost(self):
        return self.prix_m2
        print("Usine créé")


class Prix(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.ingredient.nom} coûte {self.prix}"
        f" dans le {self.departement}"

    def cost(self):
        return self.prix


class QuantiteIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"Il y a {self.quantite} de {self.ingredient.nom}"

    def cost(self, dep):
        prix_ing = self.ingredient.prix_set.get(departement__numero=dep).prix
        return prix_ing * self.quantite


class Action(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    commande = models.CharField(max_length=100)
    duree = models.IntegerField()
    ingredients = models.ManyToManyField(QuantiteIngredient)

    # action à mettre
    def __str__(self):
        return f"La {self.commande} dure {self.duree}s sur la machine"
        f" {self.machine}"


class Recette(models.Model):
    nom = models.CharField(max_length=100)
    action = models.ForeignKey(Action, on_delete=models.PROTECT)

    def __str__(self):
        return f"Recette de {self.nom}"


class Usine(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    taille = models.IntegerField()
    machines = models.ManyToManyField(Machine)
    recettes = models.ManyToManyField(Recette)
    stocks = models.ManyToManyField(QuantiteIngredient)

    def __str__(self):
        return f"L'usine du {self.departement} de taille" f" {self.taille}"

    def cost(self):
        prix_machine = 0
        prix_ingredient = 0
        for m in self.machines.all():
            prix_machine += m.cost()
        prix_entrepot = self.departement.prix_m2 * self.taille
        for n in self.stocks.all():
            prix_ingredient += n.cost(self.departement.numero)
        total = prix_machine + prix_entrepot + prix_ingredient
        return total

    def rspr(self, recette, n):
        prix_achat = 0
        for i in recette.action.ingredients.all():
            self.stocks.add(
                QuantiteIngredient.objects.create(
                    ingredient=i.ingredient, quantite=n * i.quantite
                )
            )
            prix_achat += i.cost(self.departement.numero)
        print("Prix des achats =", prix_achat)
        #    existant = 0
        #    for s in self.stocks.all():
        #        print("Dans s")
        #        if (s.ingredient == i.ingredient):
        #            print("Dans if")
        #            if(s.quantite < n*i.quantite):
        #                print("Restockage")
        #                print("new quantite", n*i.quantite)
        #                s.quantite = n*i.quantite
        #            existant = 1
        #    if ( existant == 0 ):
