import time
import googleapiclient.discovery
import json
from flask import Flask, render_template_string
import threading

# Configuration API YouTube
API_KEYS = ['YOUR_API_KEY_1', 'YOUR_API_KEY_2', 'YOUR_API_KEY_3']  
current_key_index = 0

YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# Initialiser l'API YouTube avec la première clé
youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEYS[current_key_index])

def switch_api_key():
    global current_key_index, youtube
    current_key_index = (current_key_index + 1) % len(API_KEYS)
    youtube = googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEYS[current_key_index])
    print(f"Switched to API key: {API_KEYS[current_key_index]}")

def search_music_videos(query, max_results=50):
    try:
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type="video",
            videoCategoryId="10",
        ).execute()

        return search_response.get("items", [])
    except googleapiclient.errors.HttpError as e:
        print(f"API error: {e}")
        if e.resp.status == 403:
            print("Quota exceeded, switching API key...")
            switch_api_key()
        return []

def update_blacklist(music_videos, blacklist_file='blacklist.txt'):
    try:
        existing_urls = set()
        try:
            with open(blacklist_file, 'r') as f:
                existing_urls = set(line.strip() for line in f.readlines())
        except FileNotFoundError:
            pass

        with open(blacklist_file, 'a') as f:
            for video in music_videos:
                video_url = f"https://www.youtube.com/watch?v={video['id']['videoId']}"
                if video_url not in existing_urls:
                    f.write(f"{video_url}\n")
                    existing_urls.add(video_url)
                    print(f"Added to blacklist: {video_url}")
    except Exception as e:
        print(f"Error updating blacklist: {e}")

def check_api_quota(quota_file="quota.json"):
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

# Flask application
app = Flask(__name__)

def count_urls(blacklist_file='blacklist.txt'):
    try:
        with open(blacklist_file, 'r') as f:
            return len(f.readlines())
    except FileNotFoundError:
        return 0

@app.route("/")
def index():
    url_count = count_urls()
    return render_template_string("<h1>Nombre d'URL: {{url_count}}</h1>", url_count=url_count)

def run_flask_app():
    app.run(debug=True, use_reloader=False)

# Lancer le serveur Flask dans un thread séparé
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()

def main():
    quota = check_api_quota()
    query = "music"
    
    while quota > 0:
        music_videos = search_music_videos(query, max_results=50)
        if not music_videos:
            break

        update_blacklist(music_videos)

        used_units = 100 + len(music_videos)
        update_quota(used_units)
        
        quota -= used_units
        print(f"Remaining quota: {quota}")

        time.sleep(10)

if __name__ == "__main__":
    main()
