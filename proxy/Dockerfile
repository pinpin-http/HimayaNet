# Utiliser Alpine comme base pour un conteneur léger
FROM alpine:latest

# Installer Privoxy
RUN apk add --no-cache privoxy

# Copier les fichiers de configuration
COPY privoxy-config /etc/privoxy/config
COPY block-adult.action /etc/privoxy/block-adult.action
COPY block-adult.filter /etc/privoxy/block-adult.filter

# Ajouter le fichier de modèle personnalisé
RUN mkdir -p /usr/share/privoxy/templates
COPY blocked.html /usr/share/privoxy/templates/blocked

# Exposer le port par défaut de Privoxy
EXPOSE 8118

# Commande de démarrage
CMD ["privoxy", "--no-daemon", "/etc/privoxy/config"]

