# Projet 8 : Analysez l'évolution de profils sociodémographiques avec DBT

Approfondissez vos compétences méthodologiques grâce au workflow DBT et travaillez spécifiquement sur la manière de récolter, d'analyser les données et d'utiliser DBT.

## Qu'allez-vous apprendre dans ce projet ?

Dans les projets précédents de ce parcours, vous avez appris à collecter, à traiter et à nettoyer des données.
Vous avez également découvert le règlement de protection des données personnelles. 

Dans ce nouveau projet, vous approfondirez vos compétences méthodologiques grâce au workflow DBT et travaillerez spécifiquement sur la manière de récolter, analyser les données et d'utiliser DBT.

Vous utiliserez également une solution cloud (Snowflake) pour héberger les données en interopérabilité avec DBT Cloud.

## En quoi ces compétences sont-elles importantes pour votre carrière ?

Ces compétences sont primordiales pour un data analyst : vous apprendrez à collecter vos données en vue de présenter vos résultats d'analyse.

La maîtrise de SQL, des modèles relationnels et des environnements cloud vous permettra de travailler efficacement dans des environnements data réels.

## Comment allez-vous procéder ? 

Ce projet est découpé en 2 activités.

- Ressources pédagogiques : Vous consulterez les ressources sur DBT.
- Mission : Vous réaliserez la mission principale : Analysez l'évolution du profil sociodémographique des étudiants Data d'OpenClassrooms.
    - Vous terminerez en complétant la fiche d'autoévaluation qui servira de base de discussion avec votre mentor avant la session de soutenance.

À l'issue de ce projet, vous présenterez les livrables de la mission à un mentor évaluateur lors d'une soutenance.

Cela vous permettra de valider les compétences visées par ce projet.

## Objectifs pédagogiques

- Agréger des extractions de données en définissant les règles de nettoyage
- Collecter des données pertinentes en respect des normes et bonnes pratiques
- Vérifier la cohérence et la fiabilité des données préparées

## Technologies et logiciels utilisés

![Snowflake](https://img.shields.io/badge/-Snowflake-29B5E8?logo=snowflake&logoColor=white)
![dbt Cloud](https://img.shields.io/badge/-dbt_Cloud-FF6900?logo=dbt&logoColor=white)

Pour la validation du projet OpenClassrooms (posture de Cloud Data Analyst)

![DuckDB](https://img.shields.io/badge/-DuckDB-FFA500?logo=duckdb&logoColor=white)
![dbt Core](https://img.shields.io/badge/-dbt_Core-FF6900?logo=dbt&logoColor=white)
![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/-Pandas-150458?logo=pandas&logoColor=white)

Le projet a ensuite été adapté pour ne dépendre d'aucune solution Cloud ni d'un serveur SQL grâce à [DuckDB](https://duckdb.org/).
Il s'agit d'un système de gestion de base de données embarqué, comme SQLite, mais orienté OLAP *(Online Analytical Processing)* plutôt que OLTP *(Online Transactional Processing)*.
DuckDB est capable de lire directement des fichiers CSV et supporte les modèles DBT en langage SQL et Python.
Cela permet d'utiliser la librairie Pandas pour charger des données à partir de fichiers Excel dans un format complexe *(auparavant réalisé manuellement avec Power Query)*.
