from json import dumps

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.utils.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DetailView

from .models import (
    Action,
    Departement,
    Ingredient,
    Machine,
    Prix,
    QuantiteIngredient,
    Recette,
    Usine,
    Vente,
)


class IngredientDetailView(DetailView):
    model = Ingredient

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(dumps(self.object.json_extended()))


class MachineDetailView(DetailView):
    model = Machine

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(dumps(self.object.json_extended()))


class DepartementDetailView(DetailView):
    model = Departement

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(dumps(self.object.json_extended()))


class PrixDetailView(DetailView):
    model = Prix

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(dumps(self.object.json_extended()))


class QuantiteIngredientDetailView(DetailView):
    model = QuantiteIngredient

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(dumps(self.object.json_extended()))


class ActionDetailView(DetailView):
    model = Action

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(dumps(self.object.json_extended()))


class RecetteDetailView(DetailView):
    model = Recette

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(dumps(self.object.json_extended()))


class UsineDetailView(DetailView):
    model = Usine

    def render_to_response(self, context, **response_kwargs):
        return HttpResponse(dumps(self.object.json_extended()))


@method_decorator(csrf_exempt, name="dispatch")
class VenteCreateView(CreateView):
    model = Vente

    def post(self, request, *args, **kwargs):
        self.object = None
        return super().post(request, *args, **kwargs)
