from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__, static_folder="./client", template_folder="./client")  # Настройки приложения

msg_id = 1
# all_messages = [] #Без использованияфайла db.json
DB_FILE = "db.json"

def load_messages():
    with open(DB_FILE, "r") as json_file: #Открываем файл для чтения "r"
        data = json.load(json_file)
        return data["messages"]


all_messages = load_messages() # Список сообщений,которыйзагрузитьсяизфайла


def save_messages():
    with open(DB_FILE, "w") as json_file: #Открываем файл для записи "w"
        data = {"messages": all_messages}
        json.dump(data, json_file) #Сохраняет данные в файл


@app.route("/chat")
def chat_page():
    return render_template("chat.html")


def add_message(sender, text):
    global msg_id
    new_message = {
        "sender": sender,
        "text": text,
        "time": datetime.now().strftime("%H:%M"),
        "msg_id": msg_id
    }
    msg_id += 1
    all_messages.append(new_message)
    save_messages()    # Сохраняем каждое сообщение
    # if msg_id % 10 == 0:
        # save_messages() #Сохраняем все сообщения регулярно

    #ToDo: Сохранять сообщения каждые 5 секунд, acycio
    #ToDo: Сохранять сообщения без перезаписи файла, адописывать в конец файла построчно open(file, "a")
    

# API для получения списка сообщений
# Только 5 новых сообщений: /get_messages?after=5
@app.route("/get_messages")
def get_messages():
    after = int(request.args["after"])
    return {"messages": all_messages[after:]}


# HTTP-GET
# API для получения отправки сообщения  /send_message?sender=Mike&text=Hello
@app.route("/send_message")
def send_message():
    sender = request.args["sender"]
    text = request.args["text"]
    add_message(sender, text)
    return {"result": True}


# Главная страница
@app.route("/")
def hello_page():
    return "New text goes here"


# #Приложение запускается локально на порту 5000
# app.run()

# Запуск на всех доступных интерфейсах
app.run(host="0.0.0.0", port=80)