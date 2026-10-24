# Projet de gestion de dépôt logistique

Ce projet est une application Python avec FastAPI pour gérer un dépôt logistique, avec :

- configuration personnalisable du dépôt
- ajout et suppression de palettiers (racks)
- gestion du nombre d'étages, de la taille et de la capacité par étage
- visualisation des espaces libres / occupés / partagés
- gestion de plusieurs secteurs de stockage
- zones de carton par secteur
- ajout de clients et affectation avant le stockage des palettes

## Stack

- Python 3.15.1+
- FastAPI
- SQLAlchemy + SQLite
- Jinja2 pour l'interface web

## Démarrage rapide

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Puis ouvrir :

http://localhost:8000

## Fonctionnalités principales

- Création et modification d'un dépôt
- Gestion des secteurs de stockage
- Gestion des clients
- Ajout/suppression de palettiers
- Génération automatique des emplacements selon la configuration
- Suivi de l'état d'un emplacement : libre, occupé, partagé, réservé
- Création de palettes avec affectation à un emplacement
- Dashboard de synthèse du dépôt

## Structure du projet

```text
app/
  __init__.py
  database.py
  models.py
  schemas.py
  crud.py
  main.py
  templates/index.html
```

## Exemple de flux

1. Créer un dépôt
2. Ajouter des secteurs (carton, palette, froid, etc.)
3. Ajouter des clients
4. Ajouter des palettiers
5. Générer les emplacements du rack
6. Créer des palettes et les affecter à un emplacement
7. Suivre les espaces libres ou occupés

## Notes

L'application garde les données dans une base SQLite locale `warehouse.db`.

## Compatibilité Python 3.15.1

Le problème venait de la dépendance `uvicorn[standard]`, qui chargeait `PyYAML` et provoquait une erreur de compilation sur Python 3.15.1 sous Windows.
La version actuelle du projet utilise `uvicorn` sans l'extension `standard`, ce qui évite ce point bloquant tout en gardant le serveur fonctionnel.
