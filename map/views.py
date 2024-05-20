from django.shortcuts import render, redirect
from django.http import HttpResponse
import folium
import folium.plugins
from mapproject.settings import MAPS_API_KEY, SERVICE_API_KEY

from yandex_geocoder import Client
from map.forms import RouteForm
import openrouteservice as ors
from openrouteservice.directions import directions


def route(location: list[tuple[float,float]]) -> folium.PolyLine:
    coords = location
    client = ors.Client(key=SERVICE_API_KEY)
    dir_routes = directions(client, coordinates=coords, instructions=False, preference='shortest', optimized=False)
    routes = [ p[::-1] for p in ors.convert.decode_polyline(dir_routes['routes'][0]['geometry'])['coordinates']]
    return folium.PolyLine(routes)

def index(request):
    # Create Map Object
    m = folium.Map(zoom_start=2)

    if len(request.GET.dict().keys()) != 0:
        form = RouteForm(request.GET)
        client = Client(MAPS_API_KEY)
        locations      = [ [float(x) for x in client.coordinates(v)] for k, v in form.data.dict().items() ]
        for location in locations:
            folium.Marker(location[::-1], icon=folium.Icon(color='blue')).add_to(m)
        route(locations).add_to(m)
    else:
        form = RouteForm(len=2)

    folium.plugins.Geocoder().add_to(m)

    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)
