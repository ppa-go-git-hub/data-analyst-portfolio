# OpenClassrooms, Data Analyst, Projet 8 : Analysez l'évolution de profils socio-démographiques avec dbt

À l'origine, ce projet a été réalisé avec 2 outils cloud : Snowflake et dbt Cloud. :snowflake:&times;:gear::cloud:

Cette implémentation ne dépend d'aucune ressource en ligne :
tout fonctionne en local, sans serveur SQL, grâce à DuckDB et dbt. :duck:&times;:gear:

## Installation de l'environnement

Les packets `pip` suivants sont nécessaires.

| Packet | Description |
|-|---|
| `dbt-core` | dbt (CLI) |
| `dbt-duckdb` | DuckDB + adaptateur entre dbt et DuckDB + shell interactif (duckdbt) |
| `pandas` | Librairie pour l'analyse de données |
| `openpyxl` | Dépendance de `pandas` pour lire/écrire des fichiers Excel |

Les packets `pip` suivants sont optionnels.

| Packet | Description |
|-|---|
| `python-dotenv[cli]` | Gestion des variables d'environnement d'environnement |
| `iterfzf` | Auto-complétion dans le shell interactif (duckdbt) |

## Architecture

```
data/           # Entrepôt de données (fichiers CSV/Excel)
    inputs/     # Données en entrée du pipeline
    outputs/    # Données en sortie du pipeline
dbt_project/    # Racine du projet dbt
```

:computer:
Toutes les commandes sont à exécuter dans un terminal ouvert à la racine du projet dbt.

## Configuration

### Variables d'environnement

| Nom | Description |
|-|--|
| `DBT_DUCKDB_HOME_DIRECTORY` | Paramètre de connexion DuckDB ; spécifie l'emplacement du dossier `data` |

:warning:
Il faut définir les variables d'environnement **avant** d'exécuter toute commande.

- En ligne de commande (shell Linux)

    ```sh
    export DBT_DUCKDB_HOME_DIRECTORY='../data'
    ```

- À partir d'un fichier `.env` à la racine du projet dbt

    ```
    DBT_DUCKDB_HOME_DIRECTORY='../data'
    ```

    Ajouter `dotenv run --` devant chaque commande

    ```sh
    dotenv run -- dbt build
    ```

### Variables du projet dbt

| Nom | Valeur par défaut | Description |
|-|-|--|
| `year_min` | 2022 | Première année prise en compte |
| `year_max` | 2025 | Dernière année prise en compte |

:information_source:
L'option `--vars` permet de changer ces variables.

```sh
dbt build --vars "{ year_min: 2021, year_max: 2024 }"
```

## Base de données : fichier :vs: en mémoire

Deux profils sont prédéfinis dans le fichier `dbt_project/profiles.yml`.

| Profil | Emplacement | Type de stockage | Persistant? |
|-|-|-|-|
| `default` | `dbt_project/target/P8.duckdb` | Fichier | :white_check_mark: |
| `memory` | `:memory:` | En mémoire | :x: |

Le fichier est créé à la volée lors de l'exécution des commandes dbt (s'il n'existe pas déjà).

Dans les deux cas, les données initiales et finales sont externalisées dans des fichiers CSV/Excel.

## Commandes `dbt`

Installation des dépendances (packet `dbt_utils`)
```sh
dbt deps
```

Les commandes suivantes sont pertinentes avec le profil `default` (fichier).

```sh
# Test connection (optional)
dbt debug

# Parse project (optional)
dbt parse

# Run pipeline (optional: --select <model> or --exclude <model>)
# - step-by-step
dbt seed            # Store seeds in database
dbt run             # Create stating/intermediate/mart models
dbt test            # Test models
# - all-in-one
dbt build

# Documentation
dbt docs generate   # Create
dbt docs serve      # Open in web browser
```

Les commandes suivantes sont pertinentes avec le profil `memory`.

```sh
# Parse project (optional)
dbt parse --profile memory

# Run pipeline
dbt build --profile memory

# Documentation
dbt docs generate --profile memory
dbt docs serve
```

:warning:
Ici, le pipeline ne peut pas être exécuté pas-à-pas avec une base de données en mémoire (non persistante, données perdues entre deux commandes consécutives).

## Shell interactif `duckdbt`

Exécuter l'une de ces deux commandes (en fonction du profil choisi) pour démarrer un nouveau shell interactif.
Cela lance également DuckDB (embarqué) et DuckDB UI (ouvert dans le navigateur web).

```sh
python3 -m dbt.adapters.duckdb.cli
python3 -m dbt.adapters.duckdb.cli --profile memory
```

Les commandes suivantes sont disponibles.

```sh
# Install dependencies (if not done yet)
> deps

# Test connection (optional)
> debug

# Parse project (optional)
> parse

# Run pipeline (optional: --select <model> or --exclude <model>)
# - step-by-step
> seed
> run
> test
# - all-in-one
> build
```

:bulb:
Ici, le pipeline peut être exécuté pas-à-pas même avec une base de données en mémoire (elle persiste tant que le shell interactif reste ouvert).

## Contenu de la base de données

Les sources de données sont déclarées dans un schéma fictif `csv` qui n'existe pas dans la base de données.
Après compilation, tout est remplacé par la fonction DuckDB `read_csv()`.

Les graines et les modèles sont chargés dans le schéma `dbt_dev`.

| Modèles | Matérialisation |
|-|-|
| Seeds | `table` |
| Sources | `table` |
| Staging | `view` |
| Intermediate | `view` |
| Mart | `external` |

La matérialisation externe est implémentée comme une vue qui appelle la function DuckDB `read_csv()`.

Paramètres de connexion DBeaver :beaver:

| Propriété | Valeur | Description |
|-|-|--|
| `duckdb.read_only` | `true` | Empêche DBeaver de modifier la base de données |
| `home_directory` | Emplacement du dossier `data` | Permet à DBeaver de lire les données externes |
