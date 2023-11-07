import folium
from branca.element import Figure

fig = Figure(height=550, width=750)
location1 = [51.52462680844039, -0.13406087934289235]
location2 = [51.51436828282268, -0.09846038802066716]
location3 = [51.506154348503564, -0.16893075636604676]
m = folium.Map(location1, tiles='cartodbpositron', zoom_start=13)
fig.add_child(m)

folium.Marker(location1, tooltip='Camp 1', icon=folium.Icon(color='red')).add_to(m)
folium.Marker(location2, tooltip='Camp 2', icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location3, tooltip='Camp 3', icon=folium.Icon(color='blue')).add_to(m)
m.save('map.html')
