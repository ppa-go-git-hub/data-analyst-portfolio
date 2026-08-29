Votre première analyse est déjà solide. La suite logique n’est pas d’ajouter immédiatement des modèles complexes, mais de transformer le notebook en **chaîne analytique testable, reproductible et exploitable par l’entreprise**.

Un point important doit d’abord être posé : avec uniquement un mois nommé « octobre », sans année ni date de transaction, vous pouvez analyser une **photographie de l’activité**, mais pas démontrer une saisonnalité. L’hypothèse de sur-stock avant les fêtes est métier et plausible, mais elle devra être confirmée par plusieurs millésimes d’octobre, idéalement par des données mensuelles ou transactionnelles.

## 1. Priorités recommandées

| Priorité | Objectif | Outils principaux |
|---|---|---|
| 1 | Formaliser les règles de qualité et le dictionnaire de données | Pandera, Great Expectations, dbt |
| 2 | Remplacer les fichiers CSV intermédiaires par un modèle analytique fiable | DuckDB, Parquet, dbt |
| 3 | Accélérer les traitements exploratoires | Polars, DuckDB |
| 4 | Renforcer la validité statistique | Pingouin, SciPy, statsmodels, scikit-learn |
| 5 | Rendre les résultats interprétables | SHAP, permutation importance, modèles simples |
| 6 | Surveiller les nouvelles extractions et dérives | Evidently, Great Expectations |
| 7 | Automatiser et versionner | Git, environnements verrouillés, tests, DVC ou MLflow |

La combinaison la plus pertinente pour votre contexte serait probablement :

> **Parquet + DuckDB + Polars + Pandera + dbt + Pingouin + Evidently**, avec **SHAP** uniquement si vous développez ensuite des modèles prédictifs.

---

## 2. Qualité et nettoyage des données

### Pandera — le meilleur premier ajout à votre projet

Pandera permet de décrire un schéma de DataFrame et d’y associer des contraintes directement en Python. Il est particulièrement adapté à votre situation, car vos règles sont explicites :

- prix de vente supérieur ou égal à zéro ;
- prix fournisseur supérieur ou égal à zéro ;
- stock entier et supérieur ou égal à zéro ;
- nombre de ventes entier et supérieur ou égal à zéro ;
- marge cohérente avec `prix_vente - prix_fournisseur` ;
- SKU non nul et unique ;
- catégorie appartenant à une liste contrôlée ;
- cohérence entre stock et indicateur de rupture ;
- cohérence entre ventes web et statut de publication.

Exemple simplifié :

```python
import pandera.pandas as pa
from pandera.pandas import Check, Column, DataFrameSchema

schema = DataFrameSchema(
    {
        "sku": Column(
            str,
            checks=[
                Check.str_matches(r"^[A-Za-z0-9_-]+$"),
            ],
            nullable=False,
        ),
        "prix_vente": Column(float, Check.ge(0)),
        "prix_fournisseur": Column(float, Check.ge(0)),
        "stock": Column(int, Check.ge(0)),
        "nombre_ventes": Column(int, Check.ge(0)),
        "marge": Column(float),
    },
    unique=["sku"],
    strict=False,
)

df = schema.validate(df)
```

Pour les règles inter-colonnes :

```python
schema = DataFrameSchema(
    {
        "prix_vente": Column(float, Check.ge(0)),
        "prix_fournisseur": Column(float, Check.ge(0)),
        "marge": Column(
            float,
            checks=Check(
                lambda s: (s - df["prix_vente"] + df["prix_fournisseur"]).abs() < 0.01
            ),
        ),
    }
)
```

**Évaluation :**

- **Qualité :** excellente pour formaliser des règles déterministes.
- **Robustesse :** bonne ; les contrôles sont lisibles et exécutables dans les tests automatisés.
- **Biais :** le principal risque vient de règles métier mal définies, pas de Pandera.
- **Coût :** open source, coût logiciel direct nul ; coût humain faible à modéré.
- **Temps :** faible pour commencer ; très rentable dès la deuxième extraction.
- **Reproductibilité :** excellente si les schémas sont versionnés avec le code.
- **Sécurité/conformité :** traitement local possible ; attention aux rapports contenant des descriptions ou commentaires clients.
- **Maintenabilité :** très bonne pour une équipe Python ; éviter toutefois de disperser les règles dans plusieurs notebooks.

### Great Expectations — pour industrialiser la qualité

Great Expectations est davantage orienté vers un dispositif complet de validation et de documentation : jeux d’attentes, validations, checkpoints et rapports lisibles. Ses « Data Docs » peuvent servir de preuve de qualité pour les métiers et de documentation historique des contrôles. La documentation décrit notamment les Expectations comme des assertions vérifiables et les Data Docs comme des rapports HTML regroupant attentes et résultats de validation. <citation src="1,2"></citation>

Il est bien adapté si l’entreprise souhaite :

- visualiser les résultats des contrôles ;
- conserver l’historique des validations ;
- déclencher des alertes ;
- intégrer les contrôles dans un pipeline ;
- faire intervenir des utilisateurs non développeurs.

**Comparaison pratique :**

| Critère | Pandera | Great Expectations |
|---|---|---|
| Démarrage dans un notebook | Très simple | Plus lourd |
| Règles Python | Très naturel | Possible, mais modèle plus riche |
| Documentation métier | Limitée | Très bonne |
| Tests inter-colonnes | Très adaptés | Adaptés |
| Industrialisation | À construire | Plus intégrée |
| Courbe d’apprentissage | Faible | Moyenne à élevée |
| Risque de surdimensionnement | Faible | Réel pour trois CSV mensuels |

Mon conseil : commencez par **Pandera**, puis ajoutez Great Expectations lorsque les contrôles doivent être partagés, historisés ou exécutés dans un environnement de production. Évitez de maintenir les deux pour exactement les mêmes règles, sauf si Pandera sert aux tests unitaires et Great Expectations aux contrôles de pipeline.

### Profiling automatisé : YData Profiling

YData Profiling peut générer automatiquement un rapport d’exploration contenant statistiques, valeurs manquantes, duplications, distributions, corrélations et valeurs atypiques. Il s’intègre bien à Jupyter et peut produire un rapport HTML partageable. <citation src="9"></citation>

Il est utile pour :

- comparer rapidement deux extractions ;
- détecter l’apparition d’une nouvelle catégorie ;
- repérer un changement de type ou de cardinalité ;
- documenter une première version du dataset ;
- générer une base de règles à examiner ensuite manuellement.

À utiliser comme **outil de découverte**, pas comme arbitre automatique de la qualité. Une valeur rare n’est pas nécessairement une erreur : dans votre cas, les grands crus sont précisément susceptibles d’être rares et chers. Les rapports peuvent également exposer des descriptions ou commentaires ; il faut donc filtrer les colonnes sensibles avant leur génération.

### Alternatives à examiner

- **Frictionless Data :** intéressant pour valider des fichiers tabulaires selon un schéma déclaratif.
- **Soda :** orienté data quality et monitoring, mais à évaluer selon le besoin de service hébergé.
- **Deequ :** pertinent surtout dans des environnements Spark.
- **Pydantic :** excellent pour valider des lignes ou objets d’API, moins adapté à la validation de DataFrames complets.

---

## 3. Accélération des traitements

### Polars

Polars est une alternative performante à Pandas, particulièrement intéressante avec des fichiers CSV volumineux. Son exécution paresseuse permet de construire un plan de traitement avant de l’exécuter, ce qui facilite certaines optimisations et limite les lectures inutiles. Il exploite également plusieurs cœurs dans de nombreux traitements. <citation src="6,7"></citation>

Exemple :

```python
import polars as pl

erp = pl.scan_csv("erp.csv")
web = pl.scan_csv("web.csv")
liaison = pl.scan_csv("liaison.csv")

produits = (
    erp
    .join(liaison, on="reference_erp", how="left")
    .join(web, on="sku", how="left")
    .with_columns(
        (
            pl.col("prix_vente") - pl.col("prix_fournisseur")
        ).alias("marge")
    )
    .filter(pl.col("prix_vente") >= 0)
    .collect()
)
```

**Pertinence pour votre projet :**

- lecture efficace des trois fichiers ;
- transformations typées ;
- agrégations par catégorie ;
- réduction de la consommation mémoire ;
- pipeline plus explicite que des modifications successives de DataFrame.

**Limites :**

- certaines bibliothèques statistiques et graphiques attendent encore Pandas ;
- il faudra parfois convertir avec `.to_pandas()` ;
- l’équipe doit maîtriser une nouvelle API ;
- l’exécution reste essentiellement mono-machine.

Je le recommanderais si les volumes deviennent importants ou si les notebooks commencent à devenir lents. Pour des fichiers de taille modeste, le gain de vitesse ne justifie pas forcément une migration complète.

### DuckDB

DuckDB est particulièrement adapté à votre cas : vous pouvez interroger directement les CSV ou fichiers Parquet avec SQL, effectuer des jointures, calculer des agrégats et produire des tables analytiques sans charger toute la donnée dans Pandas. Il peut aussi interroger des DataFrames Pandas ou Polars. <citation src="7"></citation>

Exemple :

```python
import duckdb

df = duckdb.sql("""
    SELECT
        w.sku,
        w.categorie,
        w.nombre_ventes,
        e.prix_vente,
        e.prix_fournisseur,
        e.stock,
        e.prix_vente - e.prix_fournisseur AS marge
    FROM read_csv_auto('web.csv') AS w
    LEFT JOIN read_csv_auto('liaison.csv') AS l
        ON w.sku = l.sku
    LEFT JOIN read_csv_auto('erp.csv') AS e
        ON l.reference_erp = e.reference_erp
""").df()
```

**Évaluation :**

- **Qualité :** excellente pour les jointures et agrégations.
- **Robustesse :** élevée pour une architecture locale mono-machine.
- **Biais :** très faible ; les risques viennent plutôt de conversions automatiques de types dans les CSV.
- **Coût :** open source et local.
- **Temps :** faible pour l’adoption, surtout si vous connaissez SQL.
- **Reproductibilité :** excellente avec des requêtes versionnées.
- **Sécurité :** bonne en local ; contrôler les extensions et accès aux fichiers distants.
- **Maintenabilité :** très bonne pour les transformations relationnelles.

DuckDB est probablement le meilleur outil pour remplacer vos fichiers CSV partitionnés par des sorties intermédiaires non documentées.

### Parquet

Même si ce n’est pas une bibliothèque Python, Parquet devrait devenir le format de stockage analytique intermédiaire :

- colonnes typées ;
- compression ;
- lecture sélective de colonnes ;
- meilleure performance que CSV ;
- conservation plus fiable des types ;
- compatibilité avec Pandas, Polars, DuckDB et de nombreux outils.

Architecture recommandée :

```text
CSV bruts
   ↓
normalisation et contrôle
   ↓
Parquet bronze
   ↓
tables nettoyées
   ↓
DuckDB / dbt
   ↓
tables analytiques et rapports
```

Conservez toujours les fichiers bruts en lecture seule et générez les tables nettoyées sans écraser la source.

---

## 4. Transformation et modèle relationnel

### dbt

dbt convient très bien à votre recommandation de refonte relationnelle. Il permet de :

- transformer les données avec SQL ;
- séparer les sources, modèles intermédiaires et modèles finaux ;
- documenter les colonnes ;
- tester unicité, non-nullité et relations ;
- visualiser les dépendances entre modèles ;
- versionner la logique de transformation.

Une organisation possible :

```text
models/
├── staging/
│   ├── stg_erp.sql
│   ├── stg_web.sql
│   └── stg_liaison.sql
├── intermediate/
│   └── int_produits_consolides.sql
└── marts/
    ├── mart_performance_produit.sql
    └── mart_performance_categorie.sql
```

Tests conceptuels :

```yaml
version: 2

models:
  - name: stg_web
    columns:
      - name: sku
        tests:
          - not_null
          - unique

  - name: int_produits_consolides
    columns:
      - name: sku
        tests:
          - not_null
          - unique
      - name: categorie
        tests:
          - not_null
```

**Évaluation :**

- **Qualité :** très bonne pour rendre les transformations explicites.
- **Robustesse :** élevée, à condition de tester les modèles.
- **Biais :** aucun biais statistique intrinsèque ; risque de logique métier incorrecte.
- **Coût :** dbt Core peut être utilisé localement ; les offres hébergées ajoutent un coût.
- **Temps :** investissement initial moyen.
- **Reproductibilité :** excellente.
- **Sécurité :** dépend fortement de la base et de l’hébergement.
- **Maintenabilité :** excellente pour une équipe travaillant avec SQL et Git.

Dans votre cas, DuckDB + dbt constitue une architecture très cohérente pour passer du notebook à un petit entrepôt analytique local.

---

## 5. Analyse statistique

### Pingouin

Pingouin est très pertinent pour approfondir votre analyse descriptive et inférentielle sans devoir écrire beaucoup de code statistique bas niveau. Il propose notamment :

- statistiques descriptives ;
- tests t ;
- tests de normalité ;
- ANOVA et alternatives non paramétriques ;
- corrélations paramétriques et non paramétriques ;
- tailles d’effet ;
- intervalles de confiance ;
- régressions ;
- tests de fiabilité ;
- correction pour comparaisons multiples ;
- analyses de puissance.

Il peut compléter efficacement Pandas, SciPy et statsmodels.

Exemples :

```python
import pingouin as pg

# Comparaison de la marge entre catégories
anova = pg.anova(
    data=df_clean,
    dv="marge",
    between="categorie",
    detailed=True
)

# Alternative non paramétrique
kruskal = pg.kruskal(
    data=df_clean,
    dv="marge",
    between="categorie"
)

# Corrélation robuste
corr = pg.corr(
    df_clean["prix_vente"],
    df_clean["prix_fournisseur"],
    method="spearman"
)

# Régression simple
reg = pg.linear_regression(
    df_clean[["prix_fournisseur"]],
    df_clean["prix_vente"]
)
```

### Ce que Pingouin peut apporter à votre étude

Votre constat de relation quasi linéaire entre prix de vente et prix fournisseur mérite d’être complété par :

1. un intervalle de confiance de la pente ;
2. un examen des résidus ;
3. une distinction entre corrélation de Pearson et de Spearman ;
4. une analyse par catégorie ;
5. une mesure de taille d’effet ;
6. une correction des tests multiples ;
7. une étude de l’hétéroscédasticité ;
8. une régression robuste si les grands crus influencent fortement la pente.

Pour la marge, ne vous limitez pas à comparer les moyennes. Utilisez aussi :

- médiane ;
- intervalle interquartile ;
- intervalle de confiance ;
- taille d’effet ;
- distribution par catégorie ;
- marge absolue et marge relative :

\[
\text{marge relative} =
\frac{\text{prix de vente} - \text{prix fournisseur}}
{\text{prix de vente}}
\]

### Limites de Pingouin

Pingouin simplifie fortement l’analyse, mais cette simplicité peut favoriser une utilisation mécanique des tests. Il ne remplace pas :

- la définition préalable d’une hypothèse ;
- la vérification des conditions du test ;
- la correction des comparaisons multiples ;
- l’analyse métier de la pertinence d’un effet ;
- statsmodels pour des modèles plus complexes ;
- SciPy pour un contrôle plus fin des méthodes numériques.

Pour votre projet, je conseillerais :

- **Pingouin** pour l’analyse statistique courante et les tailles d’effet ;
- **SciPy** pour les tests spécialisés ;
- **statsmodels** pour les modèles statistiques détaillés et les diagnostics ;
- **scikit-learn** pour la modélisation prédictive et la validation croisée.

### scikit-learn

Scikit-learn devient intéressant si vous souhaitez prévoir :

- le nombre de ventes ;
- le chiffre d’affaires ;
- le risque de rupture ;
- les produits à faible rotation ;
- une segmentation de produits ;
- une estimation du stock nécessaire.

Mais il ne faut pas l’utiliser pour fabriquer artificiellement une prédiction fiable à partir d’un seul mois. Vous aurez besoin de données historiques, idéalement :

- date ;
- prix ;
- stock ;
- catégorie ;
- promotions ;
- saison ;
- ventes quotidiennes ou hebdomadaires ;
- délai fournisseur ;
- événements commerciaux.

---

## 6. Interprétabilité et explicabilité

### SHAP

SHAP est utile lorsqu’un modèle prédictif doit être expliqué au métier. Par exemple, si vous développez un modèle de risque de rupture, SHAP peut quantifier la contribution de variables telles que :

- stock actuel ;
- catégorie ;
- prix ;
- ventes passées ;
- marge ;
- statut de publication ;
- niveau de demande.

Il permet de produire :

- une importance globale des variables ;
- une explication pour un produit particulier ;
- une analyse de l’effet positif ou négatif d’une variable ;
- des graphiques de dépendance.

**Pertinence actuelle : faible à moyenne.** Votre projet est pour l’instant principalement descriptif et statistique. SHAP deviendra pertinent lorsque vous aurez un modèle prédictif suffisamment validé.

**Points de vigilance :**

- une explication SHAP n’établit pas une causalité ;
- les variables fortement corrélées peuvent se partager artificiellement l’importance ;
- les résultats dépendent du modèle et du jeu de référence ;
- une mauvaise qualité de données produit des explications trompeuses.

Avant SHAP, utilisez d’abord :

- coefficient et intervalle de confiance d’une régression ;
- importance par permutation ;
- courbes de dépendance partielle ;
- modèles simples et facilement auditables.

---

## 7. Monitoring et dérive

### Evidently

Evidently est adapté à la comparaison de datasets ou de périodes. Vous pouvez l’utiliser pour suivre :

- évolution des distributions de prix ;
- changement de proportion des catégories ;
- hausse des valeurs manquantes ;
- nouveaux SKU ;
- variation de la proportion de ruptures ;
- dérive du nombre de ventes ;
- changement des relations entre variables.

Il serait particulièrement utile dès que vous recevrez une nouvelle extraction mensuelle. Vous pourriez comparer :

```text
octobre courant versus octobre précédent
mois courant versus mois précédent
données chargées versus données attendues
```

**Évaluation :**

- **Qualité :** bonne pour les rapports de dérive et de qualité.
- **Robustesse :** dépend du choix des métriques et seuils.
- **Biais :** un changement de distribution n’est pas nécessairement un problème ; il peut correspondre à une campagne commerciale ou à la saison.
- **Coût :** possibilité de démarrage open source ; coûts éventuels selon le mode d’hébergement.
- **Temps :** moyen.
- **Reproductibilité :** bonne si les seuils et paramètres sont versionnés.
- **Sécurité :** attention aux rapports exportés contenant des données commerciales détaillées.
- **Maintenabilité :** bonne si les métriques sont limitées à celles réellement utiles.

Great Expectations et Evidently ne font pas exactement la même chose :

- **Great Expectations :** « les données respectent-elles les règles attendues ? »
- **Evidently :** « les données ont-elles changé par rapport à une référence ? »

---

## 8. Reproductibilité et déploiement

### Git et environnement Python

Mettez sous Git :

- scripts Python ;
- notebooks ;
- requêtes SQL ;
- schémas Pandera ;
- tests ;
- fichiers de configuration ;
- dictionnaire de données ;
- résultats synthétiques ou agrégés.

Évitez de versionner les exports contenant des données commerciales sensibles. Utilisez plutôt :

- `pyproject.toml` ;
- un fichier de lock comme `uv.lock` ou `poetry.lock` ;
- Docker si l’environnement doit être reproduit sur plusieurs machines ;
- tests automatisés via `pytest`.

Structure recommandée :

```text
projet/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
│   ├── ingestion.py
│   ├── cleaning.py
│   ├── validation.py
│   └── features.py
├── models/
├── tests/
├── dbt/
├── reports/
├── pyproject.toml
└── README.md
```

Le notebook devrait devenir une couche de présentation, pas le lieu principal de la logique métier.

### DVC

DVC est intéressant si vous devez versionner de gros fichiers ou relier une version de code à une version précise des données. Il est utile pour :

- retrouver exactement le dataset utilisé pour une analyse ;
- comparer deux versions d’une extraction ;
- reproduire un rapport ;
- éviter de stocker de gros CSV dans Git.

Pour seulement trois petits fichiers mensuels, Git avec empreinte cryptographique et stockage organisé peut suffire. DVC devient justifié avec l’augmentation du volume ou le travail en équipe.

### MLflow

MLflow est à envisager seulement si vous passez à la modélisation :

- suivi des expériences ;
- paramètres ;
- métriques ;
- artefacts ;
- versions de modèles ;
- comparaison de plusieurs entraînements.

Pour l’analyse statistique actuelle, il serait probablement prématuré.

### Orchestration

Pour une exécution mensuelle :

- un script Python lancé par le planificateur système peut suffire ;
- **Prefect** est une option Python relativement accessible ;
- **Dagster** offre une approche plus structurée autour des assets ;
- **Airflow** est robuste mais probablement surdimensionné à ce stade.

N’introduisez pas un orchestrateur avant d’avoir une chaîne fonctionnelle et testée.

---

## 9. Évaluation synthétique des outils

| Outil | Rôle | Temps d’adoption | Robustesse | Reproductibilité | Maintenabilité | Priorité |
|---|---|---:|---:|---:|---:|---:|
| Pandera | Validation de DataFrames | Faible | Élevée | Élevée | Élevée | Très haute |
| Great Expectations | Qualité documentée et industrialisée | Moyen/élevé | Élevée | Élevée | Élevée | Moyenne |
| YData Profiling | Profilage automatique | Très faible | Moyenne | Bonne | Bonne | Haute |
| Polars | DataFrames performants | Moyen | Élevée | Élevée | Bonne | Moyenne/haute |
| DuckDB | SQL analytique local | Faible | Élevée | Très élevée | Très élevée | Très haute |
| Parquet | Stockage analytique | Faible | Élevée | Très élevée | Très élevée | Très haute |
| dbt | Transformations et tests SQL | Moyen | Élevée | Très élevée | Très élevée | Haute |
| Pingouin | Statistiques appliquées | Faible | Bonne | Élevée | Bonne | Très haute |
| statsmodels | Modèles statistiques détaillés | Moyen | Élevée | Élevée | Bonne | Haute |
| scikit-learn | Modélisation prédictive | Moyen | Élevée | Élevée | Très bonne | Moyenne |
| SHAP | Explicabilité de modèles | Moyen | Bonne | Bonne | Bonne | Faible actuellement |
| Evidently | Monitoring et dérive | Moyen | Bonne | Bonne | Bonne | Haute dès les données historiques |
| DVC | Versionnement de données | Moyen | Élevée | Très élevée | Bonne | Moyenne |
| MLflow | Suivi d’expériences | Moyen | Élevée | Élevée | Bonne | Faible actuellement |

---

## 10. Feuille de route concrète

### Étape 1 — rendre la donnée fiable

1. Définir le dictionnaire de données.
2. Stabiliser le format du SKU.
3. Conserver les valeurs brutes originales.
4. Créer une table de référence produit.
5. Formaliser les contrôles avec Pandera.
6. Produire un rapport d’anomalies contenant :
   - SKU ;
   - règle violée ;
   - valeur observée ;
   - valeur attendue ;
   - source ;
   - action ;
   - statut de résolution.

Ne corrigez pas silencieusement les valeurs. Préférez une colonne telle que :

```text
valeur_brute
valeur_normalisee
regle_appliquee
statut_controle
```

### Étape 2 — construire une base analytique

1. Convertir les CSV validés en Parquet.
2. Charger les fichiers dans DuckDB.
3. Créer les modèles de staging.
4. Construire une table consolidée par SKU.
5. Ajouter les tests dbt sur les clés et relations.
6. Générer des tables analytiques par produit et catégorie.

### Étape 3 — renforcer l’analyse statistique

1. Calculer les intervalles de confiance.
2. Ajouter les tailles d’effet.
3. Utiliser des tests non paramétriques lorsque nécessaire.
4. Contrôler les comparaisons multiples.
5. Diagnostiquer les résidus des régressions.
6. Comparer marge absolue et marge relative.
7. Séparer l’analyse descriptive des hypothèses causales.

### Étape 4 — suivre les extractions futures

1. Ajouter une vraie date d’extraction.
2. Ajouter l’année et le mois.
3. Si possible, récupérer la date de transaction.
4. Comparer chaque nouvelle livraison avec la précédente via Evidently.
5. Bloquer ou mettre en quarantaine les fichiers ne respectant pas les contrôles critiques.

### Étape 5 — prédire seulement lorsque l’historique sera suffisant

Avec plusieurs mois de données, vous pourrez étudier :

- prévision des ventes ;
- stock de sécurité ;
- probabilité de rupture ;
- élasticité approximative au prix ;
- segmentation des produits ;
- contribution au chiffre d’affaires et à la marge.

## Recommandation finale

Pour votre projet, je commencerais par ce socle minimal :

```text
Pandas ou Polars
        +
DuckDB
        +
Parquet
        +
Pandera
        +
dbt
        +
Pingouin
        +
Evidently
```

Puis j’ajouterais :

- **Great Expectations** si la qualité doit être présentée et historisée pour plusieurs équipes ;
- **statsmodels** pour les modèles statistiques approfondis ;
- **scikit-learn** lorsque l’historique permettra de prédire ;
- **SHAP** seulement après validation d’un modèle prédictif ;
- **DVC** ou **MLflow** lorsque le volume et le nombre d’expériences le justifieront.

Le gain principal ne viendra probablement pas d’un outil isolé, mais de la séparation claire entre **données brutes**, **données validées**, **transformations**, **analyses statistiques** et **rapports finaux**.