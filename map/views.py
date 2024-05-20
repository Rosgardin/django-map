from django.shortcuts import render, redirect
from django.http import HttpResponse
import folium
import folium.plugins
from mapproject.settings import MAPS_API_KEY

from yandex_geocoder import Client
from map.forms import RouteForm

import osmnx as ox
import osmnx.distance as oxd
import osmnx.routing as oxr
import networkx as nx

# Create your views here.

# G_walk = ox.graph_from_place( "Russia" , network_type='walk')
# G_drive = ox.graph_from_place( "Russia" , network_type='drive')

def route(start_location: tuple[float,float], end_location: tuple[float,float], type: str = 'drive') -> folium.PolyLine:
    ox.config(log_console=True, use_cache=True)

    lt, br, c = [
        [min(start_location[0], end_location[0]), min(start_location[1], end_location[1])],
        [max(start_location[0], end_location[0]), max(start_location[1], end_location[1])],
        [(start_location[0] + end_location[0]) / 2, (start_location[1] + end_location[1]) / 2]
    ]
    (n, w, s, e) = [
        [c [1],lt[0]],
        [br[1],c [0]],
        [c [1],br[0]],
        [c [1],lt[0]]
    ]
    print (f"{n=}, {w=}, {s=}, {e=}", flush=True)
    G_n = ox.graph_from_point(n)
    G_w = ox.graph_from_point(w)
    G_s = ox.graph_from_point(s)
    G_e = ox.graph_from_point(e)
    bbox = [
        ox.nearest_nodes(G_n, n[1], n[0]),
        ox.nearest_nodes(G_w, w[1], w[0]),
        ox.nearest_nodes(G_s, s[1], s[0]),
        ox.nearest_nodes(G_e, e[1], e[0])
    ]
    Gd = ox.graph_from_bbox(bbox=bbox, network_type='drive')
    orig_node = oxd.nearest_nodes(Gd,start_location[1],start_location[0])
    dest_node = oxd.nearest_nodes(Gd,end_location[1],end_location[0])
    if (orig_node == dest_node):
        return folium.Marker(start_location)
    route = nx.shortest_path(Gd, orig_node, dest_node, weight='length')

    return folium.PolyLine(route)

def index(request):
    # Create Map Object
    m = folium.Map(zoom_start=5)

    if request.GET.get('source') != None and request.GET.get('destination') != None:
        form = RouteForm(request.GET)
        client = Client(MAPS_API_KEY)
        location_source      = [float(x) for x in client.coordinates(form['source'].value())[::-1]]
        location_destination = [float(x) for x in client.coordinates(form['destination'].value())[::-1]]
        if location_source == None or location_destination == None:
            return HttpResponse('You address input is invalid')
        route(location_source, location_destination).add_to(m)
    else:
        form = RouteForm()

    folium.plugins.Geocoder().add_to(m)

    # Get HTML Representation of Map Object
    m = m._repr_html_()
    context = {
        'm': m,
        'form': form,
    }
    return render(request, 'index.html', context)
