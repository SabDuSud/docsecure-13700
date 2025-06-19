from flask import Flask, request, render_template, jsonify
import datetime
import os

app = Flask(__name__)

# Crée les fichiers de logs s'ils n'existent pas
if not os.path.exists("log_visites.txt"):
    open("log_visites.txt", "w").close()

if not os.path.exists("log_positions.txt"):
    open("log_positions.txt", "w").close()

@app.route('/')
def page():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open('log_visites.txt', 'a') as f:
        f.write(f"{now} | IP: {ip} | UA: {user_agent}\n")

    return render_template('page.html')

@app.route('/log_position', methods=['POST'])
def log_position():
    data = request.get_json()
    ip = request.remote_addr
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    lat = data.get('latitude')
    lon = data.get('longitude')

    with open('log_positions.txt', 'a') as f:
        f.write(f"{now} | IP: {ip} | Lat: {lat} | Lon: {lon}\n")

    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True)
