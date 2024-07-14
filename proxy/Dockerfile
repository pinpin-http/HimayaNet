FROM ubuntu:20.04

# Prévenir l'invite de géolocalisation pendant l'installation
ENV DEBIAN_FRONTEND=noninteractive

# Installer Squid et wget sans interaction
RUN apt-get update && apt-get install -y squid wget

# Copier les configurations de Squid
COPY config/squid.conf /etc/squid/squid.conf

# Copier le script de mise à jour des blacklists
COPY scripts/update_blacklist.sh /usr/local/bin/update_blacklist.sh
RUN chmod +x /usr/local/bin/update_blacklist.sh

# Exposer le port 3128 pour Squid
EXPOSE 3128

# Définir le point d'entrée
CMD ["/usr/local/bin/update_blacklist.sh", "&&", "squid", "-N", "-d", "1"]
