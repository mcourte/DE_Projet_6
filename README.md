# Projet : Analyse et Prédiction de la Consommation Énergétique

## Description
Ce projet vise à analyser et prédire la consommation énergétique des bâtiments à l'aide de techniques de modélisation supervisée. Il utilise des données historiques pour entraîner des modèles prédictifs et fournir des insights exploitables.

## Structure du Projet
- **Données** : Le fichier `building_energy_benchmarking.csv` contient les données utilisées pour l'analyse et la modélisation.
- **Notebook** : `nettoyage_analyse_DF.ipynb` contient le code pour l'analyse exploratoire des données et la modélisation.
- **API** : Une API est déployée pour permettre des prédictions en temps réel à l'aide de BentoML.

## Prérequis
- Python 3.8 ou supérieur
- Environnement virtuel configuré
- Bibliothèques nécessaires listées dans `requirements.txt`

## Installation

### Télécharger le code  
Cliquer sur le bouton vert <> Code puis sur Download ZIP.

Extraire l'ensemble des fichiers dans le dossier où vous souhaitez stocker le projet et les datas.

### Installer Python et ouvrir le terminal

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

Ouvrir le terminal de commande :

Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

### Créer un environnement virtuel

#### Créer l’environnement virtuel :
```
python3 -m venv venv
```

#### Activer l’environnement :

- Linux / Mac OS :
```
source venv/bin/activate
```  

- Windows :

```
venv\Scripts\activate.bat
```

#### Installer les dépendances
```
pip install -r requirements.txt
```

## Utilisation
### Analyse des Données
Ouvrez le notebook Jupyter pour explorer les données et entraîner les modèles :
```bash
jupyter notebook nettoyage_analyse_DF.ipynb
```

### Déploiement de l'API
1. Construisez le service BentoML :
   ```bash
   bentoml build
   ```
2. Démarrez le serveur BentoML :
   ```bash
   bentoml serve service:svc
   ```
3. Testez l'API avec un outil comme Postman ou curl.

## Auteur
Ce projet a été réalisé dans le cadre du parcours Data Engineer d'OpenClassrooms.

