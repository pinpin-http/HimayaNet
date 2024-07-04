# Utiliser une image de base officielle Node.js
FROM node:14

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier package.json et package-lock.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le reste du code de l'application
COPY . .

# Construire l'application pour la production
RUN npm run build

# Installer un serveur HTTP pour servir les fichiers statiques
RUN npm install -g serve

# Exposer le port que l'application va utiliser
EXPOSE 5000

# Définir la commande par défaut pour démarrer le serveur
CMD ["serve", "-s", "build"]
