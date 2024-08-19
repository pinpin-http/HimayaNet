# HimayaNet

Ce projet de contrôle parental utilise un proxy Squid pour filtrer les contenus indésirables, un backend Flask pour la gestion des configurations et un frontend React pour l'interface utilisateur.

## Structure du Projet
```sh
HimayaNet/
├── backend/             # Code pour le backend Flask
├── frontend/            # Code pour le dashboard web des parents
├── windows-app/         # Code pour l'application Windows
├── android-app/         # Code pour l'application Android
└── proxy/               # Configuration  et scripts pour le proxy Squid
```

## Prérequis

- Docker
- Docker Compose

## Installation

1. Clonez le dépôt :

   ```sh
   https://github.com/pinpin-http/HimayaNet.git
   cd HimayaNet 
   ```

 2. Assurez-vous que Docker et Docker Compose sont installés sur votre machine.

 3. Construisez et démarrez les conteneurs Docker :
 ```sh
 docker-compose build
 docker-compose up -d
```

## Utilisation
### Frontend
Le frontend React est accessible via le navigateur à l'adresse suivante :
[http://localhost:3000](http://localhost:3000)
### Backend
Le backend Flask est accessible via l'URL suivante :
[http://localhost:5000](http://localhost:5000)
### Proxy Squid
Le proxy Squid écoute sur le port 3128. Vous pouvez tester le proxy en utilisant curl :
```sh
curl -x http://localhost:3128 http://example.com
```
## Configuration
### Fichier docker-compose.yml
Le fichier **' docker-compose.yml '** configure les services pour le proxy, le backend et le frontend. Voici un aperçu de la configuration :
```yaml
version: '3.8'

services:
  proxy:
    build: ./proxy
    ports:
      - "3128:3128"
    volumes:
      - ./proxy/config:/etc/squid
      - ./proxy/scripts:/usr/local/bin

  backend:
    build: ./backend
    ports:
      - "5000:5000"
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:5000"
    volumes:
      - ./frontend:/app

```
### Configuration de Squid
Le fichier de configuration de Squid se trouve dans **' proxy/config/squid.conf '** :
```conf
# Configurer le port HTTP
http_port 3128

# Configurer les ACL pour les blacklists
acl adult_sites dstdomain "/etc/squid/blacklists/adult_sites"
http_access deny adult_sites

# Configurer les ACL par défaut
http_access allow all

# Configurer le PID
pid_filename /var/run/squid/squid.pid
```

### Script de Mise à Jour des Blacklists

Le script **' update_blacklist.sh '** se trouve dans **' proxy/scripts '** (Bloque uniquement les contenus pour adultes pour le moment):
```sh
#!/bin/bash

# URL de téléchargement de la liste noire
BLACKLIST_URL="http://dsi.ut-capitole.fr/blacklists/download/adult.tar.gz"
BLACKLIST_DIR="/etc/squid/blacklists"

# Créer le répertoire de blacklists s'il n'existe pas
if [ ! -d "$BLACKLIST_DIR" ]; then
  mkdir -p $BLACKLIST_DIR
fi

echo "Téléchargement de la liste noire depuis $BLACKLIST_URL"
wget -O /tmp/blacklist.tar.gz $BLACKLIST_URL

if [ $? -ne 0 ]; then
  echo "Échec du téléchargement de la liste noire"
  exit 1
fi

echo "Décompression de la liste noire"
tar -xzf /tmp/blacklist.tar.gz -C /tmp

if [ $? -ne 0 ]; then
  echo "Échec de la décompression de la liste noire"
  exit 1
fi

echo "Mise à jour de la liste noire"
rm -rf $BLACKLIST_DIR/*
mv /tmp/adult/* $BLACKLIST_DIR/
chown -R proxy:proxy $BLACKLIST_DIR

# Vérifier que le fichier adult_sites existe
if [ ! -f "$BLACKLIST_DIR/adult_sites" ]; then
  echo "Erreur: Le fichier $BLACKLIST_DIR/adult_sites n'existe pas"
  exit 1
fi

echo "Redémarrage de Squid"
squid -z
squid -N
```

### Dépannage
- Si un service ne démarre pas, vérifiez les logs en utilisant docker-compose logs **[service-name]**.
- Assurez-vous que les ports 3000, 5000 et 3128 ne sont pas utilisés par d'autres applications sur votre machine.

### État Actuel du Projet

**Important** : Ce projet est en cours de développement et plusieurs fonctionnalités ne sont pas encore terminées. Voici un aperçu des tâches en cours et des fonctionnalités à venir :

 - Finaliser la configuration du proxy Squid pour le filtrage des contenus indésirables.
 - Implémenter la gestion des utilisateurs et des profils dans le backend Flask.
 - Développer l'interface utilisateur pour la gestion des paramètres de contrôle   parental dans le frontend React.
- Tester et déboguer les fonctionnalités existantes pour assurer la stabilité et la fiabilité du système.
- Developper les app natives pour les plateformes Android et Windows
### Contributions
Les contributions sont les bienvenues ! Veuillez ouvrir une issue ou soumettre une pull request sur GitHub.


