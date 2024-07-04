# Utiliser une image de base Ubuntu
FROM ubuntu:20.04

# Installer Squid
RUN apt-get update && apt-get install -y squid wget

# Copier les configurations de Squid
COPY config/squid.conf /etc/squid/squid.conf
COPY blacklists /etc/squid/blacklists

# Exposer le port 3128 pour Squid
EXPOSE 3128

# Démarrer Squid en mode non-démon
CMD ["squid", "-N"]
