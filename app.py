from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

@app.route('/reserve', methods=['POST'])
def reserve():
    host = request.form['host']
    time = request.form['time']
    # Здесь нужно обработать резервирование (например, сохранить данные в базе или в файле)
    return f"ПК {host} зарезервирован на {time}"

@app.route('/')
def index():
    # В этом месте код для получения данных с Zabbix
    return render_template('index.html', message="Здесь будет статус ПК")





if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Изменение порта на 5001




def get_zabbix_data():
    url = "http://your-zabbix-server/zabbix/api_jsonrpc.php"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "your-username",
            "password": "your-password"
        },
        "id": 1
    }

    # Запрос на авторизацию
    response = requests.post(url, headers=headers, data=json.dumps(data))
    auth_token = response.json().get("result")

    # Запрос на получение хостов
    data = {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": "extend"
        },
        "auth": auth_token,
        "id": 2
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    hosts = response.json().get("result")
    return hosts
