# Aide à la prise en main du notebook

Ce document vous guide dans l'utilisation du notebook Jupyter amélioré avec l'IA : missions remplies, installation de l'environnement.

## Contexte et objectifs

L'entreprise BottleNeck a besoin d'outils professionnels pour analyser les stocks et les ventes.
Or, le système d'information est difficilement exploitable, car il est notamment composé de bases de données hétérogènes qui n'ont pas été conçues pour fonctionner ensemble.

L'objectif est double :

1. Réaliser une analyse exploratoire des données : compréhension du schéma relationnel, détection d'erreurs, mise en relation des bases de données via une table de liaison
2. Réaliser une analyse du stock et des ventes : données disponibles sur une période d'un mois, sans dates de transaction

Ces tâches sont réalisées en Python dans un notebook Jupyter.
Une version initiale utilisait Pandas et diverses librairies de visualisation (Matplotlib/Seaborn/Plotly) pour une première analyse.
Cette nouvelle version a été obtenue à l'aide de l'IA (veille technologique, assistant de code) : elle utilise Polars pour accélérer l'analyse exploratoire, et Pingouin pour approfondir l'analyse grâce aux tests statistiques.

## Architecture

```
data/               # Stockage des données
    input/          # Données en entrée (extractions au format Excel)
    output/         # Données en sortie (analyse, à vérifier)
notebook.ipynb      # Notebook Jupyter
requirements.txt    # Liste des packets Python à installer
```

## Installation de l'environnement

Voici la liste des principaux packets Python utilisées.

| Packet | Description |
|-|---|
| `notebook` | Environnement de développement Jupyter Notebook |
| `pandas` |  Librairie pour l'analyse de données (standard) |
| `polars` |  Librairie pour l'analyse de données (rapide) |
| `matplotlib` | Visualisation (statique) |
| `seaborn` | Visualisation (surcouche de Matplotlib) |
| `plotly` | Visualisation (interactive) |
| `scipy` | Statistiques (standard) |
| `pingouin` | Statistiques (interface intuitive, résultats complets) |

D'autres packets sont également nécessaires e.g. pour lire/écrire des fichiers Excel ou calculer des courbes de tendance, mais ne sont pas importés directement dans le notebook (seulement mentionnés).

Tous les packets sont listés dans le fichier `requirements.txt` et peuvent ainsi être installés en ligne de commande, par exemple avec `pip` :

```bash
pip install -r requirements.txt
```