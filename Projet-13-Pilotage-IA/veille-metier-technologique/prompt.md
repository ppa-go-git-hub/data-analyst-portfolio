Je travaille en tant que Data Analyst, spécialisé en statistiques, pour un marchand de vins et autres boissons haut de gamme.
Voici le contexte du projet sur lequel je travaille actuellement.

J'ai déjà réalisé une première analyse en Python via un notebook Jupyter (dataframes Pandas, visualisations Matplotlib/Seaborn/Plotly).
J'ai exploré, nettoyé et consolidé les données issues de trois extractions de fichiers CSV.

1. Extraction de l'ERP (référence produit, prix de vente, prix fournisseur, niveau de stock, flag rupture de stock, flag en vente sur le site web)
2. Extraction du site web (SKU, libellé, catégorie, nombre de ventes, description des produits, commentaires...) à partir d'une base de données WordPress
3. Table de liaison (correspondance référence produit ERP et SKU)

Les données portent sur le mois d'octobre, mais il n'y a pas d'autre information temporelle comme l'année ou des dates de transaction par exemple.

Dans mon analyse exploratoire, j'ai identifié des incohérences intra-colonne (e.g. valeurs négatives : prix de vente, niveau de stock, nombre de ventes)
et inter-colonnes (e.g. stock positif mais flag levé et vice versa, produit avec des ventes sur le site web mais flag ERP non levé et vice versa, valeurs négatives : colonne calculée marge = prix de vente - prix fournisseur).
Pour mon analyse, j'ai effectué une partition des produits (export dans des fichiers CSV séparés).

1. Produits sans incohérence détectée (utilisés ensuite dans l'analyse statistique)
2. Produits avec au moins une incohérence détectée (pour vérification/correction)

Dans mon analyse statistique, j'ai réalisé une analyse univariée avancée sur le prix de vente (visualisation de la distribution avec un box plot, détection d'outliers avec le Z-score et l'inter-quartile) et d'autres analyses univariées sur le chiffre d'affaires, le nombre de ventes, le niveau de stock et la marge (vision par article ou par catégorie).
J'ai aussi calculé la matrice des corrélations et identifié une relation quasi linéaire entre le prix de vente et le prix fournisseur, bien que la marge moyenne varie énormément d'une catégorie à l'autre.

Voici mes recommandations finales suite à cette première approche.

- Refonte du schéma relationnel pour atteindre la troisième forme normale, en utilisant le SKU comme identifiant produit partout (à corriger parfois pour toujours avoir un format alphanumérique) et en supprimant les colonnes redondantes (e.g. flags)
- Les outliers ne sont pas aberrants (produits très haut de gamme "grand cru" ou "premier cru").
- Le niveau de stock est élevé, ce qui peut ressembler à un excès de dépenses à première vue, mais fait sens lorsqu'on prend en compte le mois d'octobre (sur-stock en vue de satisfaire une demande saisonnière pour les fêtes de fin d'année).

L'entreprise est satisfaite de ce travail préliminaire et me laisse carte blanche pour aller plus loin.
Avant de me lancer, j'ai besoin de lister les outils actuels (de préférence liés à l'écosystème Python) qui pourraient m'être utiles.
Aide-moi dans ce travail de veille technologique, avec une présentation générale de ces outils et en expliquant en quoi ils peuvent être pertinents pour mon projet.
J'ai besoin de sources documentaires fiables (e.g. doc officielle) et d'une évaluation en termes de qualité, robustesse/biais, coût, temps, reproductibilité, sécurité/conformité, maintenabilité.

Voici quelques pistes auxquelles je pense déjà, n'hésite pas à compléter.

- Améliorer la qualité du nettoyage
- Accélérer l'analyse exploratoire
- Renforcer l'interprétabilité
- Fiabiliser le déploiement/reproductibilité