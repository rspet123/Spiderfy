import networkx as nx
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from tqdm import tqdm
SPOTIPY_CLIENT_ID = 'xx'
SPOTIPY_CLIENT_SECRET = 'xx'
max_depth = 0
depth = 0
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(SPOTIPY_CLIENT_ID,SPOTIPY_CLIENT_SECRET))
start_uri = 'Not A Uri'
search_name = "Not A Name"
artist_list = []
cont = "Y"
artist_pop = []
filter_num = -1


while not cont.upper() == "N":
    search_name = input("Search Artist: ")
    search_results = spotify.search(q='artist:' + search_name, type='artist')
    match_list = search_results["artists"]["items"]
    for i in range(len(match_list)):
        print("Index " + str(i)+" " + match_list[i]["name"])
    while start_uri == 'Not A Uri':
        try:
            index = int(input("Select Artist: "))
            start_uri = search_results["artists"]["items"][index]["uri"]
            artist_list.append(start_uri)
        except:
            print("Try That again")
    print("Selected: " + search_results["artists"]["items"][index]["name"])
    cont = input("Add Another? Y/N: ")
    start_uri = 'Not A Uri'


while max_depth == 0:
    try:
        max_depth = int(input("Enter Depth of Web: "))
    except ValueError:
        print("NaN Try again")
        
while filter_num == -1:
    try:
        filter_num = int(input("Enter Filter Number: "))
    except:
        print("Setting to 1 (Default)")
        filter_num = 1
descript = match_list[i]["name"]
visited = []
#artist_list.append(start_uri)
graph = nx.Graph()
edge_labler = {}

for d in range(max_depth):
    #depth = depth+1
    try:
        current_artist = artist_list.pop(0)
    except IndexError:
        continue
    
    album_types = ['album','single']
    artist_name = spotify.artist(current_artist)["name"]
    descript = (artist_name + " " + str(d) + '/' + str(max_depth))
    for a_type in album_types:
        results = spotify.artist_albums(current_artist, album_type=a_type)
        albums = results['items']
        
        while results['next']:
            results = spotify.next(results)
            albums.extend(results['items'])
            #relateds = spotify.artist_related_artists(current_artist)
            #print(relateds)
        for album in tqdm(albums,desc =  (descript + "|" + a_type + 's')):
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
                            #depth = depth+1
                            if not artist["uri"] == current_artist:
                                graph.add_edge(artist_name,artist["name"],label = track["name"])     
                                edge_labler[(artist_name,artist["name"])] = graph.get_edge_data(artist_name,artist["name"])["label"][0:20]
                            #Add Edge to graph
                        elif not artist["uri"] == current_artist:
                            graph.add_edge(artist_name,artist["name"])
                            #print("e") #Add Edge to graph
remove_node = []                        
for node in graph.degree():
    if node[1] < filter_num:
        remove_node.append(node[0])
graph.remove_nodes_from(remove_node)
pos = nx.spring_layout(graph)
#pos = nx.kamada_kawai_layout(graph)

nx.draw(graph,pos, with_labels=True,edge_color='pink')
#nx.draw_networkx_edge_labels(graph,pos, edge_labels = edge_labler)
print("Done")
