# Register your models here.

from django.contrib import admin

from . import models

admin.site.register(models.Ingredient)
admin.site.register(models.Machine)
admin.site.register(models.Departement)
admin.site.register(models.Prix)
admin.site.register(models.QuantiteIngredient)
admin.site.register(models.Action)
admin.site.register(models.Recette)
admin.site.register(models.Usine)
