import os
import subprocess
import json
import sys

# Liste des packages nécessaires
required_packages = [
    "google-auth",
    "google-auth-oauthlib",
    "google-auth-httplib2",
    "google-api-python-client"
]

def install_packages():
    """Installe les packages requis avec pip en utilisant --break-system-packages"""
    for package in required_packages:
        print(f"🔄 Installation du package requis : {package}...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", package, "--break-system-packages"], check=True)
            print(f"✅ Package {package} installé avec succès.")
        except subprocess.CalledProcessError:
            print(f"❌ Échec de l'installation du package {package}.")
            sys.exit(1)

# Installation des packages requis
install_packages()


import time
import random
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Nombre total de projets à gérer
TOTAL_PROJECTS_REQUIRED = 11
PROJECT_PREFIX = 'youtube-music-project'
BASE_PROJECT_PREFIX = "base-youtube-project"  # Préfixe pour le projet de base principal

# Liste des API à activer
REQUIRED_APIS = [
    "youtube.googleapis.com",
    "apikeys.googleapis.com"
]

# Codes couleurs ANSI
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Ajouter des emojis aux étapes
SUCCESS_EMOJI = "✅"
ERROR_EMOJI = "❌"
WARNING_EMOJI = "⚠️"
INFO_EMOJI = "ℹ️"
CHECK_EMOJI = "🔍"
ARROW_EMOJI = "➡️"
PROCESS_EMOJI = "🔄"

def run_command(command):
    """Exécute une commande shell et retourne sa sortie"""
    print(f"{INFO_EMOJI} {bcolors.OKBLUE}Exécution de la commande: {command}{bcolors.ENDC}")
    process = subprocess.run(command, shell=True, capture_output=True, text=True)
    if process.returncode != 0:
        print(f"{ERROR_EMOJI} {bcolors.FAIL}Erreur lors de l'exécution de la commande: {command}{bcolors.ENDC}")
        print(f"{ERROR_EMOJI} {bcolors.FAIL}{process.stderr}{bcolors.ENDC}")
        sys.exit(1)  # Arrêter le script immédiatement si une commande échoue
    return process.stdout.strip()

def check_google_cloud_sdk():
    """Vérifie si le SDK Google Cloud est installé. Si non, l'installe automatiquement."""
    sdk_installed = run_command("gcloud --version")
    if "Google Cloud SDK" not in sdk_installed:
        print(f"{WARNING_EMOJI} {bcolors.WARNING}Le SDK Google Cloud n'est pas installé. Installation en cours...{bcolors.ENDC}")
        if sys.platform.startswith("linux"):
            run_command("curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-409.0.0-linux-x86_64.tar.gz")
            run_command("tar -xf google-cloud-sdk-409.0.0-linux-x86_64.tar.gz")
            run_command("./google-cloud-sdk/install.sh")
            print(f"{SUCCESS_EMOJI} {bcolors.OKGREEN}SDK Google Cloud installé avec succès.{bcolors.ENDC}")
        else:
            print(f"{ERROR_EMOJI} {bcolors.FAIL}Installation automatique du SDK Google Cloud non prise en charge pour ce système. Installez-le manuellement.{bcolors.ENDC}")
            sys.exit(1)
    
    print(f"{SUCCESS_EMOJI} {bcolors.OKGREEN}SDK Google Cloud est installé et prêt à l'emploi.{bcolors.ENDC}")

def initialize_gcloud_sdk():
    """Initialise le SDK Google Cloud en mode non interactif"""
    print(f"{INFO_EMOJI} {bcolors.OKBLUE}Initialisation du SDK Google Cloud en mode non interactif...{bcolors.ENDC}")
    
    # Désactiver les invites
    run_command("gcloud config set disable_prompts true")

    # Authentification : Ouvre un navigateur pour choisir l'e-mail
    run_command("gcloud auth login --quiet")

    # Authentification par défaut (Application Default Credentials)
    run_command("gcloud auth application-default login --quiet")

    # Récupérer l'adresse e-mail active après authentification
    active_email = run_command("gcloud config get-value account")
    print(f"{SUCCESS_EMOJI} {bcolors.OKGREEN}Authentification réussie avec l'adresse e-mail : {active_email}{bcolors.ENDC}")

    return active_email

def find_or_create_base_project():
    """Recherche un projet de base existant ou en crée un nouveau"""
    print(f"{INFO_EMOJI} {bcolors.OKBLUE}Recherche d'un projet de base existant...{bcolors.ENDC}")
    existing_projects = list_existing_projects()
    
    # Rechercher un projet de base existant
    base_project_id = None
    for project in existing_projects:
        if project.startswith(BASE_PROJECT_PREFIX):
            base_project_id = project
            print(f"{SUCCESS_EMOJI} {bcolors.OKGREEN}Projet de base existant trouvé : {base_project_id}{bcolors.ENDC}")
            break
    
    # Si aucun projet de base n'est trouvé, en créer un nouveau
    if not base_project_id:
        base_project_id = f"{BASE_PROJECT_PREFIX}-{random.randint(1000, 9999)}"
        print(f"{INFO_EMOJI} {bcolors.OKBLUE}Création d'un nouveau projet de base '{base_project_id}'...{bcolors.ENDC}")
        run_command(f"gcloud projects create {base_project_id} --name={base_project_id}")
    
    # Activer les API requises pour le projet de base
    for api in REQUIRED_APIS + ["cloudresourcemanager.googleapis.com"]:
        enable_api(base_project_id, api)
    
    # Configurer le projet de base comme quota project
    run_command(f"gcloud auth application-default set-quota-project {base_project_id}")
    print(f"{SUCCESS_EMOJI} {bcolors.OKGREEN}Projet de quota configuré sur le projet de base '{base_project_id}'.{bcolors.ENDC}")

    return base_project_id

def enable_api(project_id, api):
    """Active une API spécifique pour un projet donné."""
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        try:
            print(f"{INFO_EMOJI} {bcolors.OKBLUE}Activation de l'API {api} pour le projet {project_id} (tentative {attempts + 1}/{max_attempts})...{bcolors.ENDC}")
            result = run_command(f"gcloud services enable {api} --project={project_id}")
            
            # Si la commande s'exécute correctement, on sort de la boucle
            if "ERROR" not in result:
                print(f"{SUCCESS_EMOJI} {bcolors.OKGREEN}API {api} activée pour le projet {project_id}{bcolors.ENDC}")
                return True
        except Exception as e:
            print(f"{ERROR_EMOJI} {bcolors.FAIL}Erreur lors de l'activation de l'API {api} pour le projet {project_id}: {e}{bcolors.ENDC}")
        
        attempts += 1
        time.sleep(15)  # Attendre avant de réessayer

    print(f"{ERROR_EMOJI} {bcolors.FAIL}Échec de l'activation de l'API {api} pour le projet {project_id}{bcolors.ENDC}")
    return False

def create_api_key_for_project(project_id):
    """Crée une clé API pour un projet existant et retourne la clé générée."""
    credentials, _ = google.auth.default()
    apikeys_service = build('apikeys', 'v2', credentials=credentials)
    
    try:
        key_body = {
            "displayName": f"API Key for {project_id}",
            "restrictions": {
                "apiTargets": [
                    {
                        "service": "youtube.googleapis.com"
                    }
                ]
            }
        }
        operation = apikeys_service.projects().locations().keys().create(
            parent=f"projects/{project_id}/locations/global",
            body=key_body
        ).execute()

        operation_name = operation.get('name')
        if operation_name:
            result = wait_for_operation(operation_name, apikeys_service)
            if result and 'response' in result:
                api_key = result['response'].get('keyString')
                if api_key:
                    print(f"{SUCCESS_EMOJI} {bcolors.OKGREEN}Clé API créée pour le projet {project_id}: {api_key}{bcolors.ENDC}")
                    return api_key
    except HttpError as e:
        print(f"{ERROR_EMOJI} {bcolors.FAIL}Erreur lors de la création de la clé API pour {project_id}: {e}{bcolors.ENDC}")
    
    return None

def list_existing_projects():
    """Retourne la liste des projets existants associés à l'utilisateur."""
    print(f"{INFO_EMOJI} {bcolors.OKBLUE}Récupération de la liste des projets existants...{bcolors.ENDC}")
    try:
        credentials, _ = google.auth.default()
        cloudresourcemanager = build('cloudresourcemanager', 'v1', credentials=credentials)
        response = cloudresourcemanager.projects().list().execute()
        projects = response.get('projects', [])
        return [proj['projectId'] for proj in projects]
    except HttpError as e:
        print(f"{ERROR_EMOJI} {bcolors.FAIL}Erreur lors de la récupération des projets: {e}{bcolors.ENDC}")
        return []

def wait_for_operation(operation_name, apikeys_service, max_attempts=30, wait_time=10):
    """Attend la fin d'une opération longue pour la création de clés API"""
    for attempt in range(max_attempts):
        print(f"{PROCESS_EMOJI} {bcolors.OKBLUE}Opération {operation_name} en cours, tentative {attempt + 1}/{max_attempts}{bcolors.ENDC}")
        result = apikeys_service.operations().get(name=operation_name).execute()
        
        if result.get("done"):
            return result
        
        time.sleep(wait_time)

    print(f"{ERROR_EMOJI} {bcolors.FAIL}L'opération {operation_name} a dépassé le temps d'attente{bcolors.ENDC}")
    return None

def main():
    check_google_cloud_sdk()
    active_email = initialize_gcloud_sdk()
    base_project_id = find_or_create_base_project()

    # Gérer les projets existants
    existing_projects = list_existing_projects()
    project_report = {}

    for project_id in existing_projects:
        if project_id.startswith(PROJECT_PREFIX):
            print(f"{INFO_EMOJI} {bcolors.OKBLUE}Traitement du projet existant : {project_id}{bcolors.ENDC}")
            for api in REQUIRED_APIS:
                enable_api(project_id, api)
            api_key = create_api_key_for_project(project_id)
            if api_key:
                project_report[project_id] = api_key

    while len(project_report) < TOTAL_PROJECTS_REQUIRED:
        project_id = f"{PROJECT_PREFIX}-{random.randint(1000, 9999)}"
        print(f"{INFO_EMOJI} {bcolors.OKBLUE}Création du projet '{project_id}'...{bcolors.ENDC}")
        run_command(f"gcloud projects create {project_id} --name={project_id}")

        for api in REQUIRED_APIS:
            enable_api(project_id, api)

        api_key = create_api_key_for_project(project_id)
        if api_key:
            project_report[project_id] = api_key

    # Sauvegarde du rapport des clés API
    with open(f"{active_email}_api_keys.json", "w") as file:
        json.dump(project_report, file, indent=4)

    print(f"{SUCCESS_EMOJI} {bcolors.OKGREEN}Script terminé avec succès. Les clés API ont été sauvegardées dans '{active_email}_api_keys.json'.{bcolors.ENDC}")

if __name__ == "__main__":
    main()
