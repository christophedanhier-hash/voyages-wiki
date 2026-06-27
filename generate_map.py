import folium

# Étapes du parcours (avec descriptions)
stops = [
    (21.0285, 105.8542, "🇻🇳 Hanoi", "J1-J3 · Capitale millénaire"),
    (20.9500, 107.0800, "🇻🇳 Baie d'Halong", "J4-J5 · UNESCO, karsts"),
    (16.4637, 107.5909, "🇻🇳 Hue", "J6 · Cité Impériale"),
    (16.2000, 108.1300, "🇻🇳 Col des Nuages", "J7 · Route panoramique"),
    (15.8801, 108.3380, "🇻🇳 Hoi An", "J7-J9 · Vieille ville aux lanternes"),
    (10.8231, 106.6297, "🇻🇳 Hô Chi Minh-Ville", "J10-J11 · Saigon"),
    (10.3515, 106.3602, "🇻🇳 Delta du Mékong", "J12 · Marchés flottants"),
    (13.3633, 103.8564, "🇰🇭 Siem Reap", "J14-J17 · Angkor"),
    (13.2000, 103.8000, "🇰🇭 Tonlé Sap", "J17 · Lac et villages flottants"),
    (11.5564, 104.9282, "🇰🇭 Phnom Penh", "J18-J19 · Capitale khmère"),
    (19.8833, 102.1333, "🇱🇦 Luang Prabang", "J20-J23 · Perle du Laos"),
    (18.9239, 102.4471, "🇱🇦 Vang Vieng", "J24-J25 · Karsts"),
    (17.9750, 102.6150, "🇱🇦 Vientiane", "J26-J27 · Capitale laotienne"),
]

# Centre approximatif de la carte
m = folium.Map(location=[17.5, 106.0], zoom_start=5, control_scale=True, tiles="OpenStreetMap")

# Segment Vietnam (index 0-6)
folium.PolyLine([(s[0], s[1]) for s in stops[:7]], color="#e63946", weight=4, opacity=0.7, popup="🇻🇳 Vietnam").add_to(m)

# Vol Saigon -> Siem Reap (ligne pointillée)
folium.PolyLine([[10.8231, 106.6297], [13.3633, 103.8564]], color="#888", weight=2, opacity=0.6, dash_array="8, 8", popup="✈️ Vol Saigon → Siem Reap").add_to(m)

# Segment Cambodge (index 7-9)
folium.PolyLine([(s[0], s[1]) for s in stops[7:10]], color="#e76f51", weight=4, opacity=0.7, popup="🇰🇭 Cambodge").add_to(m)

# Vol Phnom Penh -> Luang Prabang (ligne pointillée)
folium.PolyLine([[11.5564, 104.9282], [19.8833, 102.1333]], color="#888", weight=2, opacity=0.6, dash_array="8, 8", popup="✈️ Vol Phnom Penh → Luang Prabang").add_to(m)

# Segment Laos (index 10-12)
folium.PolyLine([(s[0], s[1]) for s in stops[10:13]], color="#2a9d8f", weight=4, opacity=0.7, popup="🇱🇦 Laos").add_to(m)

# Marqueurs
for i, (lat, lon, name, desc) in enumerate(stops):
    if i == 0:
        color = "green"
        icon_type = "flag"
    elif i == len(stops) - 1:
        color = "red"
        icon_type = "flag"
    else:
        color = "blue"
        icon_type = "info-sign"
    
    folium.Marker(
        [lat, lon],
        popup=f"<b>{name}</b><br>{desc}",
        tooltip=name,
        icon=folium.Icon(color=color, icon=icon_type)
    ).add_to(m)

# Légende HTML
legend_html = '''
<div style="position:fixed; bottom:30px; left:10px; z-index:1000; background:white;
     padding:10px; border-radius:8px; font-size:12px; border:1px solid #ccc; max-width:200px;">
<b>🗺️ Vietnam-Laos-Cambodge</b><br>
🔴 🇻🇳 Vietnam (route)<br>
🟠 🇰🇭 Cambodge (route)<br>
🟢 🇱🇦 Laos (route)<br>
- - - ✈️ Vol interne<br>
🟢 Début · 🔚 Fin<br><br>
<b>28 jours — ~1 800 km</b>
</div>'''
m.get_root().html.add_child(folium.Element(legend_html))

m.save("/opt/data/voyages-wiki/docs/vietnam-laos-cambodge-2027/carte-vietnam-laos-cambodge.html")
print("✅ Carte générée avec succès !")
