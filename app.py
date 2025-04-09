from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/reserve', methods=['POST'])
def reserve():
    host = request.form['host']
    time = request.form['time']
    # Здесь можно добавить логику для сохранения данных о резервировании (например, в базу данных)
    return f"ПК {host} зарезервирован на {time}"

@app.route('/')
def index():
    # Получаем данные с Zabbix
    hosts = get_zabbix_data()
    return render_template('index.html', message="Здесь будет статус ПК", hosts=hosts)

def get_zabbix_data():
    url = "http://192.168.100.250/zabbix/api_jsonrpc.php"
    headers = {
        "Content-Type": "application/json"
    }
    
    # Используйте свой API токен
    auth_token = "d21afa4160a0826fe5966fdbe71001c19fa6e310fba7beeced2456aa8db2f783"  # Ваш токен из Zabbix

    # Запрос на получение хостов
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
    hosts = response.json().get("result")
    return hosts
if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Изменение порта на 5001
