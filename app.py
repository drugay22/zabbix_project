from flask import Flask, render_template, request
import requests
import json
import logging

# Настройка логирования
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

@app.route('/reserve', methods=['POST'])
def reserve():
    logging.debug("Processing reserve request...")
    host = request.form['host']
    time = request.form['time']
    logging.debug(f"Host: {host}, Time: {time}")
    return f"ПК {host} зарезервирован на {time}"

@app.route('/')
def index():
    logging.debug("Fetching data from Zabbix...")
    hosts = get_zabbix_data()
    logging.debug(f"Fetched {len(hosts)} hosts from Zabbix.")
    return render_template('index.html', message="Здесь будет статус ПК", hosts=hosts)

def get_zabbix_data():
    url = "http://192.168.100.250:8080/zabbix/api_jsonrpc.php"
    headers = {
        "Content-Type": "application/json"
    }
    
    # Используйте свой API токен
    auth_token = "d21afa4160a0826fe5966fdbe71001c19fa6e310fba7beeced2456aa8db2f783"  # Ваш токен из Zabbix
    logging.debug("Sending request to Zabbix API...")

    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": "extend"
        },
        "auth": auth_token,  # Используем ваш токен
        "id": 2
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Проверка ответа
    if response.status_code != 200:
        logging.error(f"Error fetching data from Zabbix: {response.status_code}, {response.text}")
        return []

    try:
        hosts = response.json().get("result")
        logging.debug(f"Received {len(hosts)} hosts from the response.")
        return hosts
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON from Zabbix API response.")
        return []

if __name__ == "__main__":
    logging.debug("Starting Flask application...")
    app.run(debug=True, port=5001)  # Изменение порта на 5001
