FROM ubuntu:22.04

# Installer Squid
RUN apt-get update && apt-get install -y squid apache2-utils

# Copier la configuration de Squid
COPY squid.conf /etc/squid/squid.conf

# Copier la page de blocage et les styles
RUN mkdir -p /var/www/html/block
COPY blocked.html /var/www/html/block/
COPY style.css /var/www/html/block/

# Autoriser les fichiers web
RUN chmod -R 755 /var/www/html/block/

# Exposer le port par défaut de Squid
EXPOSE 3128

# Commande pour démarrer Squid
CMD ["squid", "-N", "-f", "/etc/squid/squid.conf"]

