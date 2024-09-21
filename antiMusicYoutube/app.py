from flask import Flask, render_template_string
import threading

app = Flask(__name__)

# Fonction pour compter les URLs
def count_urls(blacklist_file='blacklist.txt'):
    try:
        with open(blacklist_file, 'r') as f:
            return len(f.readlines())
    except FileNotFoundError:
        return 0

# Route principale
@app.route("/")
def index():
    url_count = count_urls()
    return render_template_string("<h1>Nombre d'URL: {{url_count}}</h1>", url_count=url_count)

def run_flask_app():
    app.run(debug=True, use_reloader=False)

# Lancement du serveur Flask dans un thread séparé
flask_thread = threading.Thread(target=run_flask_app)
flask_thread.start()
