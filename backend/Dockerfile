# Utiliser une image de base officielle Python
FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier le fichier des dépendances
COPY requirements.txt requirements.txt

# Installer les dépendances
RUN pip install -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port que l'application va utiliser
EXPOSE 5000

# Définir la commande par défaut pour démarrer l'application
CMD ["python", "app.py"]
