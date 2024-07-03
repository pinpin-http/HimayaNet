#!/bin/bash

# URL de téléchargement de la liste noire
BLACKLIST_URL="http://dsi.ut-capitole.fr/blacklists/download/adult.tar.gz"
BLACKLIST_DIR="/etc/squid/blacklists"

# Télécharger la liste noire
wget -O /tmp/blacklist.tar.gz $BLACKLIST_URL

# Vérifier si le téléchargement a réussi
if [ $? -ne 0 ]; then
  echo "Échec du téléchargement de la liste noire"
  exit 1
fi

# Décompresser la liste noire
tar -xzf /tmp/blacklist.tar.gz -C /tmp

# Vérifier si la décompression a réussi
if [ $? -ne 0 ]; then
  echo "Échec de la décompression de la liste noire"
  exit 1
fi

# Mettre à jour la liste noire
rm -rf $BLACKLIST_DIR/*
mv /tmp/adult/* $BLACKLIST_DIR/

# Vérifier si le conteneur existe avant de redémarrer Squid
if [ $(docker ps -q -f name=my-proxy) ]; then
  # Redémarrer Squid pour appliquer les changements
  docker exec my-proxy squid -k reconfigure
else
  echo "Le conteneur my-proxy n'existe pas"
fi
