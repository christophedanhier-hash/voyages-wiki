#!/opt/hermes/.venv/bin/python3
"""
🌀 Polarsteps Voyages Extractor
Extrait les données de voyage Polarsteps → JSON + Markdown
Usage: echo 'ton_token' | ./polarsteps_extract.py
       Ou: POLARSTEPS_TOKEN='XXX' ./polarsteps_extract.py
"""
import os, sys, json, time, re
from datetime import datetime
from pathlib import Path

import requests

# ─── Config ───────────────────────────────────
API_BASE = "https://api.polarsteps.com"
API_VERSION = "52"
USERNAME = "christophedanhier"
DATA_DIR = Path("/opt/data/voyages-data")
WIKI_DIR = Path("/tmp/voyages-wiki-content")
MAX_RETRIES = 5
RETRY_DELAY = 2

# ─── Auth setup ───────────────────────────────
token = (sys.stdin.readline().strip() if not sys.stdin.isatty()
         else os.environ.get('POLARSTEPS_TOKEN', ''))
if not token:
    print("❌ FOURNIS TON TOKEN : echo 'token' | python3 polarsteps_extract.py")
    sys.exit(1)

SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)',
    'Accept': 'application/json',
    'Cookie': f'remember_token={token}',
    'Polarsteps-API-Version': API_VERSION,
})

def api_get(path):
    """GET with retry logic for 502 CloudFront errors."""
    url = f"{API_BASE}{path}"
    for attempt in range(MAX_RETRIES):
        try:
            r = SESSION.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
            if r.status_code == 502:
                wait = RETRY_DELAY * (attempt + 1)
                print(f"  ⚠️  502 retry {attempt+1}/{MAX_RETRIES} in {wait}s...")
                time.sleep(wait)
                continue
            r.raise_for_status()
        except Exception as e:
            if attempt == MAX_RETRIES - 1:
                print(f"  ❌ {path}: {e}")
                return None
            time.sleep(RETRY_DELAY)
    return None

def fmt_date(iso_str):
    """Parse ISO date to readable format."""
    try:
        d = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return d.strftime('%d/%m/%Y')
    except:
        return iso_str[:10] if iso_str else '?'

def fmt_duration(start, end):
    """Calculate duration in days."""
    try:
        s = datetime.fromisoformat(start.replace('Z', '+00:00'))
        e = datetime.fromisoformat(end.replace('Z', '+00:00'))
        return (e - s).days + 1
    except:
        return 0

def emoji_country(country_code):
    """Convert country code to flag emoji."""
    if not country_code or len(country_code) != 2:
        return '🌍'
    return chr(ord(country_code[0]) + 127397) + chr(ord(country_code[1]) + 127397)

def slugify(name):
    """Create a URL-safe slug from trip name."""
    s = name.lower().strip()
    s = re.sub(r'[^\w\s-]', '', s)
    s = re.sub(r'[-\s]+', '-', s)
    return s.strip('-')

# ─── MAIN ─────────────────────────────────────
DATA_DIR.mkdir(parents=True, exist_ok=True)
WIKI_DIR.mkdir(parents=True, exist_ok=True)

print("🌀 Polarsteps Voyages Extractor")
print("=" * 50)

# 1. Récupérer profil utilisateur
print("\n📋 Profil utilisateur...")
user = api_get(f"/users/byusername/{USERNAME}")
if not user:
    print("❌ Impossible de récupérer le profil")
    sys.exit(1)

print(f"   ✅ {user['first_name']} {user['last_name']}")
print(f"   🌍 {user['stats']['country_count']} pays, "
      f"{int(user['stats']['km_count']):,} km, "
      f"{user['stats']['trip_count']} voyages, "
      f"{user['stats']['step_count']} étapes")

# Save user data
with open(DATA_DIR / 'user.json', 'w') as f:
    json.dump(user, f, indent=2, default=str)
print(f"   💾 user.json sauvegardé")

# 2. Récupérer chaque voyage en détail
print("\n🗺️ Détails des voyages...")
trips = user.get('trips', [])
all_trips_data = []

for i, t in enumerate(trips):
    tid = t['id']
    name = t.get('name', 'Sans nom')
    vis = '🔒' if t.get('visibility') == 1 else '🌐'
    print(f"\n   {vis} [{tid}] {name}")

    details = api_get(f"/trips/{tid}")
    if details:
        steps = details.get('steps', [])
        print(f"      → {len(steps)} étapes, {details.get('total_km', '?')} km")
        all_trips_data.append(details)

        # Save raw JSON
        slug = slugify(name)
        with open(DATA_DIR / f'trip_{tid}_{slug}.json', 'w') as f:
            json.dump(details, f, indent=2, default=str)
        print(f"      💾 trip_{tid}_{slug}.json")
    else:
        # Fallback: use data from user response
        all_trips_data.append(t)
        print(f"      ⚠️ Données partielles (user endpoint)")

    time.sleep(0.5)  # Polite delay between requests

# 3. Generate Markdown files for wiki
print("\n\n📝 Génération pages wiki...")

# --- Index page ---
vis_count = sum(1 for t in trips if t.get('visibility') == 2)
priv_count = sum(1 for t in trips if t.get('visibility') == 1)
countries = user['stats'].get('country_codes', [])
country_flags = ' '.join(emoji_country(c) for c in countries)

index_md = f"""# 🧭 Voyages de Christophe

*Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M')}*

---

## 🌍 En chiffres

| | |
|---|---|
| **Pays visités** | {user['stats']['country_count']} {country_flags} |
| **Distance totale** | {int(user['stats']['km_count']):,} km |
| **Étapes enregistrées** | {user['stats']['step_count']} |
| **Voyages réalisés** | {vis_count} |
| **Voyages en cours/privés** | {priv_count} |
| **Followers** | {len(user.get('followers', []))} |

---

## 🗺️ Liste des voyages

| Voyage | Période | Durée | Distance | Statut |
|--------|---------|:-----:|:--------:|:------:|
"""

for t in sorted(trips, key=lambda x: x.get('start_date', '') or '', reverse=True):
    name = t.get('name', '?')
    start = fmt_date(t.get('start_date', ''))
    end = fmt_date(t.get('end_date', ''))
    duration = fmt_duration(t.get('start_date', ''), t.get('end_date', ''))
    km = int(t.get('total_km', 0)) if t.get('total_km') else '?'
    vis = '🔒 Privé' if t.get('visibility') == 1 else '🌐 Public'
    slug = slugify(name)
    index_md += f"| [{name}]({slug}/) | {start} → {end} | {duration}j | {km:,} km | {vis} |\n" if isinstance(km, int) else f"| [{name}]({slug}/) | {start} → {end} | {duration}j | ? km | {vis} |\n"

index_md += """
---

## 🚀 Voyages à venir

*Section à compléter — préparation, itinéraires, réservations.*

---

*Données extraites depuis [Polarsteps](https://www.polarsteps.com/christophedanhier/)*
"""

with open(WIKI_DIR / 'index.md', 'w') as f:
    f.write(index_md)
print("   ✅ index.md")

# --- Trip pages ---
for t in sorted(trips, key=lambda x: x.get('start_date', '') or '', reverse=True):
    name = t.get('name', 'Voyage sans nom')
    slug = slugify(name)
    vis = '🔒 Privé' if t.get('visibility') == 1 else '🌐 Public'
    start = fmt_date(t.get('start_date', ''))
    end = fmt_date(t.get('end_date', ''))
    duration = fmt_duration(t.get('start_date', ''), t.get('end_date', ''))
    km = int(t.get('total_km', 0)) if t.get('total_km') else 0

    # Get full details
    details = next((d for d in all_trips_data if d.get('id') == t['id']), None)
    steps = (details or t).get('steps', [])
    if not steps:
        steps = (details or t).get('all_steps', [])

    # Find countries visited
    countries_visited = set()
    locations_visited = []
    for s in steps:
        loc = s.get('location', {}) or {}
        cc = loc.get('country_code', '')
        if cc:
            countries_visited.add(emoji_country(cc) + ' ' + (loc.get('country', '') or ''))
        if loc.get('locality') or loc.get('name'):
            locations_visited.append(loc.get('locality') or loc.get('name') or '?')

    countries_str = ', '.join(sorted(countries_visited)) if countries_visited else 'N/A'
    photos = sum(len(s.get('media', []) or []) for s in steps)
    likes = details.get('like_count', 0) if details else 0

    page = f"""# {name}

{vis} · {start} → {end} · {duration} jours · {km:,} km

---

## 📊 Résumé

| | |
|---|---|
| **Date début** | {start} |
| **Date fin** | {end} |
| **Durée** | {duration} jours |
| **Distance** | {km:,} km |
| **Étapes** | {len(steps)} |
| **Photos** | {photos} |
| **Pays visités** | {countries_str} |
| **Visibilité** | {vis} |

## 🗺️ Itinéraire

"""

    # Print steps table
    for i, s in enumerate(steps):
        loc = s.get('location', {}) or {}
        step_name = s.get('name') or loc.get('name') or loc.get('locality') or f'Étape {i+1}'
        lat = loc.get('lat', '?')
        lon = loc.get('lon', '?')
        desc = s.get('description', '')
        has_photos = len(s.get('media', []) or [])
        photo_icon = ' 📸' if has_photos else ''
        wth = ''
        if s.get('weather_condition'):
            wth = f' · {s["weather_condition"]} {s.get("weather_temperature", "")}°C'
        desc_text = f' — {desc[:80]}' if desc and desc != step_name else ''
        page += f"1. **{step_name}**{photo_icon} [{lat:.4f}, {lon:.4f}](https://maps.google.com/?q={lat},{lon}){desc_text}{wth}\n"

    # Photos section
    all_media = []
    for s in steps:
        for m in (s.get('media', []) or []):
            all_media.append(m)
    if all_media:
        page += f"\n## 📸 Photos ({len(all_media)})\n\n"
        for m in all_media[:20]:
            url = m.get('cdn_path') or m.get('path', '')
            desc = m.get('description', '')
            if url:
                page += f"![]({url})\n\n"
                if desc:
                    page += f"*{desc}*\n\n"

    # Navigation
    page += f"\n---\n\n[⬅️ Retour à l'index](../)\n"

    trip_dir = WIKI_DIR / slug
    trip_dir.mkdir(parents=True, exist_ok=True)
    with open(trip_dir / 'index.md', 'w') as f:
        f.write(page)
    print(f"   ✅ {slug}/index.md")

# 4. Save metadata
meta = {
    'extracted_at': datetime.now().isoformat(),
    'username': USERNAME,
    'user_id': user.get('id'),
    'trip_count': len(trips),
    'total_km': int(user['stats']['km_count']),
    'total_steps': user['stats']['step_count'],
    'country_count': user['stats']['country_count'],
    'api_version': API_VERSION,
}
with open(DATA_DIR / 'metadata.json', 'w') as f:
    json.dump(meta, f, indent=2)
print(f"   ✅ metadata.json")

# 5. Summary
print("\n" + "=" * 50)
print(f"✅ Extraction terminée !")
print(f"   📁 Données brutes : {DATA_DIR}")
print(f"   📁 Pages wiki    : {WIKI_DIR}")
print(f"   📄 {len(trips)} voyages extraits")
print(f"   📸 {sum(len(d.get('steps', [])) for d in all_trips_data)} étapes total")
print(f"\nPour utiliser : copier {WIKI_DIR}/* dans un repo MkDocs")
