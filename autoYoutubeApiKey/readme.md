
# YouTube API Key automatisation 

Ce script Python permet de créer, gérer et configurer automatiquement plusieurs projets Google Cloud pour l'utilisation de l'API YouTube Data v3. Il gère la création de projets, l'activation des API nécessaires.
L'output est un fichier Json contenant un couple projet:token

# 📋 Fonctionnalités Principales
- **Création automatique de projets Google Cloud** : Le script crée les projets nécessaires en respectant un quota de 12 projets par session. (1 projet pilote et 11 projet avec l'api ytb data v3 )
- **Activation des API requises** : Il active l'API YouTube Data v3 et l'API Key Management pour chaque projet de facon automatisé et sécurisé.
- **Gestion des quotas ** : Utilise un projet de base (projet pilote) pour les quotas afin d'optimiser l'utilisation des clés d'API.
- **Génération de clés d'API** : Génère et sauvegarde les clés d'API pour chaque projet.
- **Rapport JSON** : Sauvegarde les clés d'API dans un fichier JSON nommé avec l'adresse e-mail utilisée.

# 🛠️ Prérequis
- ***Python 3.6 ou supérieur***
- ***Compte Google***
et c'est tout....

# 📦 Installation des dépendances

Le script gère automatiquement l'installation des packages nécessaires via  ```pip ```:
```python
# Packages requis
required_packages = [
    "google-auth",
    "google-auth-oauthlib",
    "google-auth-httplib2",
    "google-api-python-client"
]

# Fonction d'installation des packages
def install_packages():
    for package in required_packages:
        subprocess.run([sys.executable, "-m", "pip", "install", package, "--break-system-packages"], check=True)

```
Si vous souhaitez installer les packages manuellement, exécutez :
```bash 
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client --break-system-packages

```

# 🔧 Utilisation du Script
 **1 - Téléchargez le script** et placez-le dans votre répertoire de travail.
 
 **2 - Exécutez le script :**
 ```bash 
 python autoYtProj.py
```

 **3 - Authentification :** Le script vous demandera de vous connecter à votre compte Google pour authentifier votre session.

 **4 - Création et gestion des projets :** Le script prend la main apres ca et gère la création, l'activation des API, et la génération des clés d'API.


# 🧠 Fonctionnalités détaillées

### 1. Vérification et installation du SDK Google Cloud
-  ```python check_google_cloud_sdk() ```: Vérifie si le SDK est installé, l'installe si nécessaire, puis initialise l'environnement.

### 2. Initialisation du SDK Google Cloud
-  ```initialize_gcloud_sdk() ```:  Configure l'environnement pour une authentification sans invites, puis effectue l'authentification de l'utilisateur.

### 3. Recherche ou création d'un projet de base
-  ```find_or_create_base_project() ```:  Cherche un projet de base existant ou en crée un nouveau. Ce projet est utilisé pour gérer les quotas de l'API.

### 4. Activation des API nécessaires
-  ```enable_api(project_id, api)```:  Active une API spécifique pour un projet donné avec plusieurs tentatives en cas d'échec.

### 5. Création de clés d'API
-  ```create_api_key_for_project(project_id) ```:  Crée une clé d'API pour un projet donné et gère les erreurs éventuelles.

### 6. Sauvegarde des clés d'API générées
-  ```main() ```:   La fonction principale gère le flux global du script, de la création des projets à la sauvegarde des clés d'API dans un fichier JSON.

# 📂 Rapport final

Le script génère un fichier JSON nommé avec l'adresse e-mail utilisée ( ```  example@gmail.com_api_keys.json ```). Ce fichier contient un dictionnaire avec les identifiants des projets et leurs clés d'API associées.

# 📌 Exemple de fichier JSON de sortie
```json
    {
    "youtube-music-project-1234": "AIzaSyA1B...",
    "youtube-music-project-5678": "AIzaSyB2C..."
    }
```


## FAQ

#### Q : Que faire si le SDK Google Cloud n'est pas installé ?
R : Le script le détecte et l'installe automatiquement.
#### Q : Pourquoi une authentification est-elle nécessaire et quelles informations sont recupérés? 

R : L'authentification est requise pour permettre au script d'accéder à Google Cloud et de gérer les projets et les API. Le script ne peut pas accéder a vos informations personelle, il est limité aux informations publique.

#### Q : Le script génère-t-il toujours de nouvelles clés ?
R : Oui, il crée toujours une nouvelle clé d'API, même si l'API est déjà activée pour un projet. Donc en sortie vous obtiendrez toujours 11 clés d'api.
