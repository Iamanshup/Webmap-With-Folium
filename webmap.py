import folium
import pandas

#function to get color for the markers according to the heights
def getColour(elevation):
    if elevation < 2000: return 'green'
    elif 2000<= elevation < 3000: return 'orange'
    else: return 'red'

#read file and store the required data in lists
data = pandas.read_csv('volcanoes.csv')
lat = list(data['LAT'])
lon = list(data['LON'])
name = list(data['NAME'])
elev = list(data['ELEV'])

#create an object of folium.folium.Map
map = folium.Map(location = [lat[0], lon[0]], zoom_start = 6, tiles = 'Mapbox Bright')

#create an object of folium.Map.FeatureGroup to store the features of 1st layer
fgv = folium.FeatureGroup(name = 'Volcanoes')
for lt, ln, n, el in zip(lat, lon, name, elev):
    fgv.add_child(folium.Marker(location = [lt, ln], popup = folium.Popup(html = n+', '+str(el)+' m', parse_html = True), icon = folium.Icon(color = getColour(el))))
    fgv.add_child(folium.CircleMarker(location = [lt, ln], popup = folium.Popup(html = n+', '+str(el)+' m', parse_html = True), radius = 5, fill_color = getColour(el), color = 'grey', fill_opacity = 0.7))

#create an object of folium.Map.FeatureGroup to store the features of 2nd layer
fgp = folium.FeatureGroup(name = 'Population')
fgp.add_child(folium.GeoJson(data = open('world.json', 'r', encoding = 'utf-8-sig').read(),
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 else 'orange' if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)

#add a layer control
map.add_child(folium.LayerControl())

map.save('Map1.html')
