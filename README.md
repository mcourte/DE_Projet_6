# Projet : Analyse et Prédiction de la Consommation Énergétique - Seattle

*Description*  
Ce projet vise à prédire la consommation énergétique et les émissions de CO2 des bâtiments de la ville de Seattle. Il s'inscrit dans une démarche de Smart City pour identifier les bâtiments à haute priorité d'optimisation énergétique.
Le projet inclut une chaîne complète : du nettoyage des données à la mise en production d'une API de prédiction robuste via BentoML, intégrée dans un environnement Cloud.

## Structure du Projet

- notebooks/ : Analyse exploratoire (EDA), ingénierie des caractéristiques et sélection du modèle (Gradient Boosting).

- api/ : Code source de l'API de production.

   - service.py : Logique de service BentoML avec validation Pydantic.

   - bentofile.yaml : Configuration du packaging du modèle.

   - pyproject.toml : Gestion moderne des dépendances avec Poetry.

models/ : Modèles entraînés et enregistrés via le Bento Store.

## Installation & Développement local
### 1. Prérequis
  
- Python 3.11 ou supérieur
  
- Azure CLI (pour le déploiement Cloud)
  
- Poetry (gestionnaire de dépendances)
  
  
**Etape 1 : Télécharger le code**

Cliquer sur le bouton vert <> Code puis sur Download ZIP.

Extraire l'ensemble des fichiers dans le dossier où vous souhaitez stocker le projet et les datas.

**Etape 2 : Installer Python et ouvrir le terminal**

Télécharger [Python](https://www.python.org/downloads/) et [installer-le](https://fr.wikihow.com/installer-Python)  

- Ouvrir le terminal de commande :

   -Pour les utilisateurs de Windows : [démarche à suivre ](https://support.kaspersky.com/fr/common/windows/14637#block0)  
   -Pour les utilisateurs de Mac OS : [démarche à suivre ](https://support.apple.com/fr-fr/guide/terminal/apd5265185d-f365-44cb-8b09-71a064a42125/mac)  
   -Pour les utilisateurs de Linux : ouvrez directement le terminal de commande   

**Etape 3 : Créer un environnement virtuel**

*Créer l’environnement virtuel :*
```
python3 -m venv env
```

*Activer l’environnement :*

- Linux / Mac OS :
```
source env/bin/activate
```  

- Windows :

```
env\Scripts\activate.bat
```

**Etape 4 : Installer les dépendances**
```
pip install -r requirements.txt
```
### 2. Gestion des dépendances avec Poetry
Nous utilisons Poetry pour isoler les dépendances de production et de développement.


**Installation de Poetry (via pip dans l'environnement virtuel)**
```
python -m pip install poetry
```
**Installation des dépendances verrouillées**
```
python -m poetry install
```

### 3. Construction du Bento
Le "Bento" regroupe le code, le modèle et les dépendances dans une unité prête pour le déploiement.

```
bentoml build
```
  
### 4. Tests et Validation de l'API (Local)  
Avant le déploiement, il est recommandé de tester l'API localement pour vérifier la validation Pydantic.  
  
Démarrer le serveur :  
```
cd api
bentoml serve service:EnergyService --reload
```
L'interface Swagger est alors accessible sur : [localhost](http://localhost:3000)  

-Scénarios de test de validation :  

  
   - Validation de type : Envoyer une chaîne de caractères pour une surface déclenche une erreur 422.  
  
   - Validation de plage : Une année de construction inférieure à 1850 est automatiquement rejetée.
  
   - Intégrité : L'absence de colonnes requises par le modèle (ex: ComplianceStatus) est signalée immédiatement.

    
## Déploiement Azure (Workflow Industriel)
En raison de restrictions de sécurité sur le poste de travail professionnel (absence de droits administrateur pour Docker/WSL), le déploiement est réalisé via Azure Container Registry (ACR) en mode Cloud Build.

### 1. Build de l'image sur le Cloud
Le build de l'image Docker est délégué à Azure à partir du Bento généré localement :

- Se placer dans le dossier exporté du Bento
```
az acr build --registry <NOM_REGISTRE_ACR> --image energy-service:latest .
```

### 2. Déploiement sur Azure Container Instances (ACI)
L'image est ensuite instanciée sur Azure Container Instances, exposant l'API sur le port 3000.

## Utilisation de l'API
Une fois l'API déployée, l'interface Swagger (Interactive Docs) est accessible via : http://[AZURE_DNS_OU_IP]:3000/docs

- Validation des données (Pydantic)
L'API intègre une validation stricte. Exemple de payload JSON pour l'endpoint /predict :

```
JSON

{  
  "data": {  
    "PropertyGFATotal": 55000,  
    "PropertyGFABuilding(s)": 50000,  
    "NumberofBuildings": 1,  
    "NumberofFloors": 10,  
    "YearBuilt": 1990,  
    "LargestPropertyUseTypeGFA": 45000,  
    "BuildingType": "NonResidential",  
    "PrimaryPropertyType": "Hotel",  
    "Neighborhood": "DOWNTOWN",  
    "LargestPropertyUseType": "Hotel",  
    "ListOfAllPropertyUseTypes": "Hotel"  
  }  
}  
```
## Auteur
Ce projet a été réalisé par mcourte dans le cadre du parcours Data Engineer d'OpenClassrooms.
