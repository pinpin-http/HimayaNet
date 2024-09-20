FROM ubuntu:20.04

# Prévenir l'invite de géolocalisation pendant l'installation
ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances nécessaires (Squid, wget, et utilitaires pour gérer les logs et répertoires)
RUN apt-get update && \
    apt-get install -y squid wget curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Créer les répertoires pour Squid
RUN mkdir -p /var/log/squid /var/run/squid /etc/squid/blacklists && \
    chown -R proxy:proxy /var/log/squid /var/run/squid /etc/squid

# Copier la configuration Squid dans le conteneur
COPY config/squid.conf /etc/squid/squid.conf

# Copier le script de mise à jour des blacklists
COPY scripts/update_blacklist.sh /usr/local/bin/update_blacklist.sh

# Donner les droits d'exécution au script
RUN chmod +x /usr/local/bin/update_blacklist.sh

# Créer un fichier PID et attribuer les permissions
RUN touch /var/run/squid/squid.pid && \
    chown -R proxy:proxy /var/run/squid/squid.pid

# Exposer le port 3128 pour Squid
EXPOSE 3128

# Définir l'utilisateur Squid
USER proxy

# Définir le point d'entrée : mise à jour des blacklists, initialisation de Squid, et lancement en mode débogage
CMD ["/bin/bash", "-c", "/usr/local/bin/update_blacklist.sh && squid -N -d 1"]
    