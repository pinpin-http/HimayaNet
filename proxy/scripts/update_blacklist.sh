#!/bin/bash

# URL de téléchargement de la liste noire
BLACKLIST_URL="http://dsi.ut-capitole.fr/blacklists/download/adult.tar.gz"
BLACKLIST_DIR="/etc/squid/blacklists"

# Créer le répertoire de blacklists s'il n'existe pas
if [ ! -d "$BLACKLIST_DIR" ]; then
  mkdir -p $BLACKLIST_DIR
fi

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
chown -R proxy:proxy $BLACKLIST_DIR

# Lister le contenu du répertoire de blacklists
echo "Contenu de $BLACKLIST_DIR après mise à jour:"
ls -l $BLACKLIST_DIR

# Vérifier que les fichiers essentiels existent
if [ ! -f "$BLACKLIST_DIR/domains" ] || [ ! -f "$BLACKLIST_DIR/urls" ]; then
  echo "Erreur: Les fichiers essentiels dans $BLACKLIST_DIR n'existent pas"
  exit 1
fi

echo "Redémarrage de Squid"
squid -z
squid -N
