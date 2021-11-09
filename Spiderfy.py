# Spotify API Test
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import spotipy
import os
from spotipy.oauth2 import SpotifyClientCredentials
# Porter Robinson: 3dz0NnIZhtKKeXZxLOxCam
# Seven Lions: 6fcTRFpz0yH79qSKfof7lp
# Last Heros: 3HHfEn7yPOy3IiHS6CHG97
# Caster: 4z7OnrBHTHdfpjNKl7NGox
SPOTIPY_CLIENT_ID = 'xx'
SPOTIPY_CLIENT_SECRET = 'xx'
max_depth = 100
depth = 0
start_uri = 'spotify:artist:3dz0NnIZhtKKeXZxLOxCam'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET))
artist_list = []
visited = []
artist_list.append(start_uri)
graph = nx.Graph()
edge_labler = {}

while depth < max_depth:
    depth = depth+1
    current_artist = artist_list.pop(0)
    artist_name = spotify.artist(current_artist)["name"]
    graph.add_node(artist_name)
    results = spotify.artist_albums(current_artist, album_type='album')
    albums = results['items']
    
    while results['next']:
        results = spotify.next(results)
        albums.extend(results['items'])
    
    for album in albums:
        #print("Album Name:" + album["name"] +" ID"+ album["id"])
        tracks = spotify.album_tracks(album["id"])
        for track in tracks["items"]:
            #print("Track: " + track["name"])
            artists = track["artists"]
            #print("Artists")
            for artist in artists:
                #print("\t"+artist["name"])
                if artist["uri"] not in artist_list:
                    if artist["uri"] not in visited:
                        artist_list.append(artist["uri"])
                        visited.append(artist["uri"])
                        graph.add_node(artist["name"])
                        graph.add_edge(artist_name,artist["name"],label = track["name"])     
                        edge_labler[(artist_name,artist["name"])] = graph.get_edge_data(artist_name,artist["name"])["label"][0:20]
                        #Add Edge to graph
                    elif not artist["uri"] == current_artist:
                        graph.add_edge(artist_name,artist["name"])
                        #print("e") #Add Edge to graph
pos = nx.spring_layout(graph)
nx.draw(graph,pos, with_labels=True,edge_color='pink')
#nx.draw_networkx_edge_labels(graph,pos, edge_labels = edge_labler)
print("done")