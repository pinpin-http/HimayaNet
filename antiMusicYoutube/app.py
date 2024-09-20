import time
import googleapiclient.discovery
import json

# Configuration API YouTube
API_KEY = ''
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Initialiser l'API YouTube
youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

def search_music_videos(query, max_results=50):
    try:
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type="video",  # Filtrer uniquement les vidéos
            videoCategoryId="10",  # Limite aux vidéos musicales
        ).execute()

        return search_response.get("items", [])
    except googleapiclient.errors.HttpError as e:
        print(f"API error: {e}")
        if e.resp.status == 403:
            print("Quota exceeded, waiting for reset...")
            time.sleep(24 * 60 * 60)  # Attendre 24 heures avant de réessayer
        return []

def update_blacklist(music_videos, blacklist_file='blacklist.txt'):
    try:
        with open(blacklist_file, 'a') as f:
            for video in music_videos:
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                f.write(f"{video_url}\n")
                print(f"Added to blacklist: {video_url}")
    except Exception as e:
        print(f"Error updating blacklist: {e}")

def check_api_quota(quota_file="quota.json"):
    # Utilise une gestion manuelle du quota pour éviter de dépasser la limite
    try:
        with open(quota_file, 'r') as f:
            quota_data = json.load(f)
        return quota_data.get("quota_available", 10000)
    except FileNotFoundError:
        return 10000

def update_quota(used_units, quota_file="quota.json"):
    try:
        with open(quota_file, 'r+') as f:
            quota_data = json.load(f)
            quota_data["quota_available"] -= used_units
            f.seek(0)
            f.write(json.dumps(quota_data))
            f.truncate()
    except FileNotFoundError:
        with open(quota_file, 'w') as f:
            json.dump({"quota_available": 10000 - used_units}, f)

def main():
    quota = check_api_quota()
    query = "music"
    
    while quota > 0:
        music_videos = search_music_videos(query, max_results=50)
        if not music_videos:
            break

        update_blacklist(music_videos)

        used_units = 100 + len(music_videos)  # 100 unités pour la recherche, 1 unité par vidéo récupérée
        update_quota(used_units)
        
        quota -= used_units
        print(f"Remaining quota: {quota}")

        # Pause entre les requêtes pour éviter de trop solliciter l'API
        time.sleep(10)

if __name__ == "__main__":
    main()
