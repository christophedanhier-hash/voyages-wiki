# Voyages Wiki 🧭

Carnet de voyages alimenté depuis Polarsteps — [Voir le site](https://christophedanhier-hash.github.io/voyages-wiki/)

## Structure

```
voyages-wiki/
├── docs/               # Pages du wiki (Markdown)
│   ├── index.md        # Accueil
│   ├── italie/         # Voyages à venir
│   ├── france-espagne-portugal/
│   └── ...
├── mkdocs.yml          # Configuration MkDocs
├── .github/workflows/  # Auto-déploiement GH Pages
└── polarsteps_extract.py  # Script d'extraction (manuel)
```

## Extraire un nouveau voyage

```bash
echo 'ton_token' | python3 polarsteps_extract.py
```

Le script produit des fichiers Markdown prêts pour le wiki + les données brutes en JSON.
