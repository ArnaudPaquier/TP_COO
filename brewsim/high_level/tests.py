from django.test import TestCase

from .models import Departement, Ingredient, Machine, Prix, QuantiteIngredient, Usine

# class MachineModelTests(TestCase):
#    def test_usine_creation(self):
#        self.assertEqual(Machine.objects.count(), 0)
#        Machine.objects.create(nom="four",prix=1_000)
#        self.assertEqual(Machine.objects.count(), 1)


class UsineModelTests(TestCase):
    def test_usine_creation(self):
        self.assertEqual(Usine.objects.count(), 0)
        self.assertEqual(Machine.objects.count(), 0)
        self.assertEqual(Prix.objects.count(), 0)
        self.assertEqual(Departement.objects.count(), 0)
        self.assertEqual(Ingredient.objects.count(), 0)

        four = Machine.objects.create(nom="four", prix=1_000)
        cuve = Machine.objects.create(nom="cuve", prix=2_000)
        houblon = Ingredient.objects.create(nom="houblon")
        orge = Ingredient.objects.create(nom="orge")
        hg = Departement.objects.create(numero=31, prix_m2=2_000)
        Prix.objects.create(ingredient=houblon, departement=hg, prix=20)
        Prix.objects.create(ingredient=orge, departement=hg, prix=10)
        houblon50 = QuantiteIngredient.objects.create(ingredient=houblon, quantite=50)
        orge100 = QuantiteIngredient.objects.create(ingredient=orge, quantite=100)

        usine = Usine.objects.create(departement=hg, taille=50)

        usine.machines.add(four)
        usine.machines.add(cuve)
        usine.stocks.add(houblon50)
        usine.stocks.add(orge100)

        self.assertEqual(Usine.objects.first().cost(), 105_000)

        print("><><><><><><><><><><><><><><><><><")
        print("Prix Usine = ", usine.cost())
        print("><><><><><><><><><><><><><><><><><")
