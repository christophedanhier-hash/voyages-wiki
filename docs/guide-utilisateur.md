---
date: 2026-06-26
author: LEO
version: 1.0
---

# 🧭 Guide Utilisateur — Bot Voyage Sylvia

> Bienvenue sur le bot voyage BAVI LEO ! Ce guide t'explique comment utiliser Sylvia, ce qu'elle peut faire pour toi, et comment ça marche.

---

## 🌍 Présentation

**Sylvia** est une agence de voyage complète. Elle t'aide à :

- Planifier **tous types de voyages** : camping-car 🚐, voiture 🚗, avion ✈️, train 🚄, moto 🏍️
- Trouver **le meilleur hébergement** : campings, hôtels, locations (Airbnb, gîte), aires CC, auberges
- Organiser **les transports** : location vélo 🚲, moto, voiture, billets train/avion, ferries ⛴️
- Créer des **itinéraires multi-transports** combinant différents moyens
- Générer des **cartes interactives** du parcours
- Respecter tes **contraintes** (accessibilité, budget, durée)
- Estimer ton **budget voyage** complet

---

## 💬 Comment lui parler

### Sur Telegram

👉 **@bavi_leo_voyages_bot**

Tu peux lui parler directement en DM ou dans un groupe. Pas besoin de syntaxe spéciale — parle-lui en français, comme à un ami.

**Exemples de questions :**
```
- "Prépare-moi un roadbook pour l'Italie en septembre"
- "Quel camping près de Florence pour un CC de 8m ?"
- "Météo à Vérone la première semaine d'octobre ?"
- "Ajoute une étape à Sienne entre Florence et Rome"
```

### Temps de réponse

- ⚡ Questions simples : 2-5 secondes
- 📋 Roadbook complet : quelques minutes (recherche web + cartes)
- 🗺️ Carte interactive : 10-20 secondes

---

## 🚫 Ce qu'elle fait (et ne fait pas)

| ✅ **Peut faire** | ❌ **Ne peut pas faire** |
|:-----------------|:------------------------|
| Roadbooks camping-car, voiture, train, avion | Code, programmation |
| Hôtels, campings, locations, aires CC, auberges | Finances et placements |
| Location vélo, moto, voiture | Santé et médical |
| Itinéraires multi-transports | Recettes de cuisine |
| Cartes OSM interactives | Tout sujet hors voyage |
| Billets train/avion, ferries | |
| Budget voyage complet | |

En cas de demande hors sujet, Sylvia répondra :
> *"Navré, je suis Sylvia — ton agence de voyage 🌍 Je ne réponds qu'aux questions de voyages (camping-car, train, avion, hôtel, location...)."*

---

## 💳 Tarification

Deux formules selon ton profil :

| Qui | Abonnement | Roadbooks |
|:----|:----------:|:-----------|
| 🧑‍✈️ **Christophe** (propriétaire) | **0 €** | Tokens IN/OUT réels uniquement |
| 👥 **Amis** (Pascal…) | **12 €/an** | Tokens IN/OUT + **2,50 €** forfait par dossier |

**L'abonnement** (12 €/an) démarre le **1er du mois** de ton premier dossier. Il inclut :
- Chat illimité (questions météo, campings, vérifications)
- Accès au bot sans limite de messages
- Mises à jour et améliorations du service

**Le forfait dossier** (2,50 €) s'ajoute pour chaque roadbook complet livré avec :
- Session de travail dédiée
- Fichier structuré dans le wiki
- Carte interactive du parcours
- Archivage git + commit

**Exemple concret :**

| Utilisateur | **💶 Total** | Abonnement | Roadbooks | Tokens | Forfait |
|:------------|:-----------:|:----------:|:----------|:------:|:-------:|
| 🧑‍✈️ **Christophe** | **0,14 €** | 0 € | 🇮🇹 Italie | 0,14 € | 0 € |
| 🤖 **Pascal** | **19,73 €** | 12 €/an | 🇳🇴🇫🇷🇪🇸 (3) | 0,23 € | 7,50 € |

---

## 📋 Comment se déroule une session

### Chat rapide (inclus dans l'abonnement)
```
① Tu poses une question (météo, camping, info)
② Sylvia répond directement
③ Terminé — pas de fichier, pas de commit
```

### Roadbook complet (forfait dossier)
```
① Tu demandes un roadbook
② Sylvia planifie le parcours (recherche web, cartes)
③ Tu valides les étapes
④ Sylvia génère le fichier + carte interactive
⑤ Commit dans le wiki + push
⑥ Tu reçois le lien
```

---

## ❓ FAQ

**Q : Puis-je utiliser Sylvia sans abonnement ?**
R : Si tu es invité, l'abonnement 12 €/an est requis pour le chat. Christophe n'a pas d'abonnement.

**Q : Que se passe-t-il si je pose une question hors voyage ?**
R : Sylvia refusera poliment et te rappellera son rôle.

**Q : Mes données de voyage sont-elles privées ?**
R : Oui, les roadbooks sont stockés dans le wiki privé BAVI LEO.

**Q : Puis-je modifier un roadbook après sa création ?**
R : Oui, il suffit de redemander à Sylvia de le compléter — elle ajoutera les modifications.

**Q : Comment sont calculés les coûts ?**
R : Les tokens DeepSeek sont facturés au prix réel ($0,15/M IN, $0,60/M OUT pour le Flash). Le forfait 2,50 € couvre le service (recherche, cartes, wiki, git).

---

*Dernière mise à jour : 26/06/2026 — Généré par [BAVI LEO](https://christophedanhier-hash.github.io/BAVI_LEO/)*
