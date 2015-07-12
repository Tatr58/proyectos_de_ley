# -*- encoding: utf-8 -*-
from django.shortcuts import render

from . import forms
from pdl.models import Proyecto
from pdl.models import Seguimientos
from pdl.utils import do_pagination
from pdl.utils import convert_date_to_string


def index(request):
    if request.method == 'GET':
        form = forms.SearchAdvancedForm(request.GET)
        if form.is_valid():
            print(">>cleaned_data", form.cleaned_data)
            if form.cleaned_data['date_from'] is not None:
                return search_by_date(form, request)

            if form.cleaned_data['comision'].strip() != '':
                return search_by_comission(form, request)

            if form.cleaned_data['dispensados_2da_votacion'] == 'TOTAL dispensados':
                return search_dispensados_todos(form, request)

            if form.cleaned_data['dispensados_2da_votacion'] == 'NÚMERO TOTAL DE LEYES':
                return search_total_leyes(form, request)

            return render(request, "search_advanced/index.html", {
                "form": form,
            })
        else:
            return render(request, "search_advanced/index.html", {
                "form": form,
            })


def search_by_date(form, request):
    date_from = form.cleaned_data['date_from']
    date_to = form.cleaned_data['date_to']
    queryset = Proyecto.objects.filter(
        fecha_presentacion__range=(date_from, date_to)).order_by('-codigo')
    obj = do_pagination(request, queryset, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "date_from": convert_date_to_string(date_from),
        "date_to": convert_date_to_string(date_to),
    })


def search_by_comission(form, request):
    comision = form.cleaned_data['comision']
    if comision.lower() == 'ciencia':
        comision = 'Ciencia'
    queryset = Seguimientos.objects.order_by('-proyecto_id')
    proyectos = Proyecto.objects.order_by('-codigo')
    proyects_found = []
    this_proyecto_id = ''
    for i in queryset:
        if i.proyecto_id != this_proyecto_id:
            if comision in i.evento:
                for proyecto in proyectos:
                    if i.proyecto_id == proyecto.id:
                        proyects_found.append(proyecto)
                        continue
        this_proyecto_id = i.proyecto_id
    obj = do_pagination(request, proyects_found, search=True,
                        advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })


def search_dispensados_todos(form, request):
    total_dispensed = [i.proyecto for i in Seguimientos.objects.select_related('proyecto').filter(
                       evento__icontains='dispensado 2da')]

    obj = do_pagination(request, total_dispensed, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(total_dispensed),
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })


def search_total_leyes(form, request):
    are_law = Proyecto.objects.exclude(
        titulo_de_ley__isnull=True).exclude(
        titulo_de_ley__exact='')

    obj = do_pagination(request, are_law, search=True, advanced_search=True)
    return render(request, "search_advanced/index.html", {
        "result_count": len(are_law),
        "extra_result_msg": "Total número de proyectos que han generado leyes",
        "items": obj['items'],
        "pretty_items": obj['pretty_items'],
        "first_half": obj['first_half'],
        "second_half": obj['second_half'],
        "first_page": obj['first_page'],
        "last_page": obj['last_page'],
        "current": obj['current'],
        "form": form,
        "comision": obj['comision'],
    })
