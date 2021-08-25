# Predichoc - Une application d'estimation des risques
[![Build Status](https://travis-ci.com/SimplonAI/api-mmo.svg?token=54ssNXAp4tdWQ5mk1zsT&branch=main)](https://travis-ci.com/SimplonAI/api-mmo) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Notre application se base sur les data publiques gouvernementales de 2019.

# Prérequis
* Python 3.9
* PostgreSQL
ou
* Docker
    * Suivre seulement l'étape Docker

# Installation
```console
git clone https://github.com/Assurance-Project-secure-road/predi-choc
cd predi-choc
python -m venv venv
```
Sur Windows exécutez :
```console
venv/Scripts/activate
```
ou sur Linux :
```console
source venv/bin/activate
```
Ensuite finir par :
```console
pip install -r requirements.txt
```

# Configuration
Ouvrir le fichier `exemple_config.yml` et remplacer les valeurs par défaut par celle de votre environnement. Copier ensuite ce fichier dans un dossier instance et le renommer config.yml.
```console
mkdir instance
cp exemple_config.yml instance/config.yml
```
Ensuite exécuter les commandes de configuration pour la BDD:
```console
flask db upgrade
flask insert-db
```

# Créer un utilisateur
Afin d'utiliser l'app, vous allez devoir vous connecter avec un utilisateur. Pour le créer :
```console
flask create-user
```

# Exécution
Pour lancer l'app, vous devrez taper la commande :
```console
flask run
```

# Docker
Si vous voulez vous éviter toutes les instructions précédentes, il est conseillé d'utiliser Docker.
## Configuration
Il faut configurer les variables environnements de Postgres dans un fichier .env à placer à la racine de l'application (renommer le fichier `.env.exemple` en `.env` suffit amplement) :
```console
cp .env.exemple .env
```
## Construire et exécuter l'image docker :
```console
docker-compose up -d
```
## Connexion au conteneur de l'appplication et création d'un utilisateur:
1. Lister les conteneur actif :
```console
docker ps
```
2. Selectionner le "CONTAINER_ID" du conteneur "api-mmo_website"

3. Connecter vous au bash du conteneur et crée l'utilisateur de l'application Flask:
```console
docker exec -it "CONTAINER_ID" flask create-user
```
4. De la même manière il sera possible d'exécuter les autres commandes flask.
