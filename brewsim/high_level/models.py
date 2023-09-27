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
        return f"{self.nom} {self.prix}"

    def cost(self):
        return self.prix


class Departement(models.Model):
    numero = models.IntegerField()
    prix_m2 = models.IntegerField()

    def __str__(self):
        return f"{self.numero} {self.prix_m2}"

    def cost(self):
        return self.prix_m2


class Prix(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    prix = models.IntegerField()

    def __str__(self):
        return f"{self.ingredient} {self.departement} {self.prix}"

    def cost(self):
        return self.prix


class QuantiteIngredient(models.Model):
    ingredient = models.ForeignKey(Ingredient, on_delete=models.PROTECT)
    quantite = models.IntegerField()

    def __str__(self):
        return f"{self.ingredient} {self.quantite}"


class Action(models.Model):
    machine = models.Foreignkey(Machine, on_delete=models.PROTECT)
    commande = models.CharField(max_length=100)
    duree = models.IntegerField()
    ingredients = models.ManyToManyField(QuantiteIngredient)
    # action à mettre

    def __str__(self):
        return f"{self.machine} {self.commande} {self.duree} {self.ingredients}"


class Recette(models.Model):
    nom = models.CharField(max_length=100)
    action = models.ForeignKey(Action, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.nom} {self.action}"


class Usine(models.Model):
    departement = models.ForeignKey(Departement, on_delete=models.PROTECT)
    taille = models.IntegerField()
    machines = models.ManyToManyField(Machine)
    recettes = models.ManyToManyField(Recette)
    stocks = models.ManyToManyField(QuantiteIngredient)

    def __str__(self):
        return (
            f"{self.departement} {self.taille} {self.machines}"
            f"{self.recettes} {self.stocks}"
        )

    def cost(self):
        price = 0
        for m in self.machines:
            price += m.prix

        return price + self.departement.prix_m2 * self.taille
