# mysite/models.py
from django.db import models


class Ingredient(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom}"

    def json(self):
        return {"nom": self.nom}

    def json_extended(self):
        return self.json()


class Machine(models.Model):
    nom = models.CharField(max_length=100)
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.nom}"

    def cost(self):
        return self.prix

    def json(self):
        return {"nom": self.nom, "prix": self.prix}

    def json_extended(self):
        return self.json()


class Departement(models.Model):
    numero = models.IntegerField()
    prix_m2 = models.IntegerField()

    def __str__(self):
        return f"Département {self.numero}"

    def cost(self):
        return self.prix_m2
        print("Usine créé")

    def json(self):
        return {"numero": self.numero, "prix_m2": self.prix_m2}

    def json_extended(self):
        return self.json()


class Prix(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.ingredient.nom} coûte {self.prix}"
        f" dans le {self.departement}"

    def cost(self):
        return self.prix

    def json(self):
        return {
            "ingredient": self.ingredient.id,
            "departement": self.departement.id,
            "prix": self.prix,
        }

    def json_extended(self):
        return {
            "ingredient": self.ingredient.json_extended(),
            "departement": self.departement.json_extended(),
            "prix": self.prix,
        }


class QuantiteIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"Il y a {self.quantite} de {self.ingredient.nom}"

    def cost(self, dep):
        prix_ing = self.ingredient.prix_set.get(departement__numero=dep).prix
        return prix_ing * self.quantite

    def json(self):
        return {"ingredient": self.ingredient.id, "quantite": self.quantite}

    def json_extended(self):
        return {
            "ingredient": self.ingredient.json_extended(),
            "quantite": self.quantite,
        }


class Action(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.PROTECT)
    commande = models.CharField(max_length=100)
    duree = models.IntegerField()
    ingredients = models.ManyToManyField(QuantiteIngredient)

    # action à mettre
    def __str__(self):
        return f"La {self.commande} dure {self.duree}s sur la machine"
        f" {self.machine}"

    def json(self):
        tab = []
        for i in self.ingredients.all():
            tab.append(i.id)
        return {
            "machine": self.machine.id,
            "commande": self.commande,
            "duree": self.duree,
            "ingredients": tab,
        }

    def json_extended(self):
        tab = []
        for i in self.ingredients.all():
            tab.append(i.json_extended())
        return {
            "machine": self.machine.json_extended(),
            "commande": self.commande,
            "duree": self.duree,
            "ingredients": tab,
        }


class Recette(models.Model):
    nom = models.CharField(max_length=100)
    action = models.ForeignKey(Action, on_delete=models.PROTECT)

    def __str__(self):
        return f"Recette de {self.nom}"

    def json(self):
        return {"nom": self.nom, "action": self.action.id}

    def json_extended(self):
        return {"nom": self.nom, "action": self.action.json_extended()}


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
        print("Prix des achats (models.Model):=", prix_achat * n, "€")

    def json(self):
        tabm = []
        tabr = []
        tabs = []

        for m in self.machines.all():
            tabm.append(m.id)
        for r in self.recettes.all():
            tabr.append(r.id)
        for s in self.stocks.all():
            tabs.append(s.id)

        return {
            "departement": self.departement.id,
            "taille": self.taille,
            "machines": tabm,
            "recettes": tabs,
            "stocks": tabs,
        }

    def json_extended(self):
        tabm = []
        tabr = []
        tabs = []

        for m in self.machines.all():
            tabm.append(m.json())
        for r in self.recettes.all():
            tabr.append(r.json_extended())
        for s in self.stocks.all():
            tabs.append(s.json_extended())

        return {
            "departement": self.departement.json_extended(),
            "taille": self.taille,
            "machines": tabm,
            "recettes": tabs,
            "stocks": tabs,
        }


class Vente(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    benefices = models.IntegerField()
