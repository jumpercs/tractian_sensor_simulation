import flask as f
import firebase_admin
from firebase_admin import credentials, messaging
import json
import time
from flask import jsonify, request
from collections import defaultdict
from datetime import datetime, timedelta

# Inicialização do Firebase
cred = credentials.Certificate("./serviceAccountKey.json")
firebase_admin.initialize_app(cred)
app = f.Flask(__name__)

# Variáveis Globais
last_send_time = 0
notification_interval = 300  # 5 minutos em segundos

@app.route("/send-notification", methods=["POST"])
def send_notification():
    try:
        data = request.json
        if can_send_notification():
            send_push_notification(data["device_token"], data["title"], data["message"])
            return jsonify({"status": "success"})
        else:
            return jsonify({"status": "error", "message": "Notification sent too frequently"}), 429
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/fetch-history', methods=["GET"])
def fetch_history():
    try:
        data = []
        with open("data.json", "r") as f:
            lines = f.readlines()
            for line in lines[-60:]:
                data.append(json.loads(line))
        return jsonify({"data": data})
    except FileNotFoundError:
        return jsonify({"status": "error", "message": "data.json not found"}), 404
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/fetch-aggregated-history', methods=["GET"])
def fetch_aggregated_history():
    try:
        aggregated_data = []
        vibration_data = defaultdict(list)
        
        # Agrupar os dados em intervalos de 5 minutos
        with open("data.json", "r") as f:
            lines = f.readlines()
            for line in lines:
                data = json.loads(line)
                timestamp = datetime.fromtimestamp(data["timestamp"])
                interval_key = timestamp.replace(minute=timestamp.minute - timestamp.minute % 5, second=0, microsecond=0)
                vibration_data[interval_key].append(data["vibration"])

        now = datetime.now()
        interval_start = now.replace(minute=now.minute - now.minute % 5, second=0, microsecond=0)

        for i in range(12):  # Última 1 hora (12 intervalos de 5 minutos)
            interval_end = interval_start + timedelta(minutes=5)
            if interval_start in vibration_data:
                interval_values = vibration_data[interval_start]
                if interval_values:
                    avg_vibration = sum(interval_values) / len(interval_values)
                    aggregated_data.append({
                        "intervalStart": interval_start.strftime("%Y-%m-%d %H:%M:%S"),
                        "intervalEnd": interval_end.strftime("%Y-%m-%d %H:%M:%S"),
                        "average_vibration": avg_vibration
                    })
            interval_start -= timedelta(minutes=5)

        aggregated_data.reverse()  # Ordena do mais antigo para o mais recente
        return jsonify({"data": aggregated_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

def can_send_notification():
    global last_send_time
    current_time = time.time()
    return current_time - last_send_time > notification_interval

def send_push_notification(device_token, title, message):
    global last_send_time
    message = messaging.Message(
        notification=messaging.Notification(
            title=title + ' - ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            body=message,
        ),
        android=messaging.AndroidConfig(
            priority='high',
        ),
        condition= "'maquina_1' in topics"
    )

    response = messaging.send(message)
    last_send_time = time.time()
    print('Successfully sent message:', response)

if __name__ == "__main__":
    app.run(debug=True)
