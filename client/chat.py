from utils import set_timeout, fetch

last_seen_id = 0
# Находим элементы интерфейса по их ID
send_message = document.getElementById("send_message")
sender = document.getElementById("sender")
message_text = document.getElementById("message_text")
chat_window = document.getElementById("chat_window")
emoji_selector = document.getElementById("emoji_selector")

# Добавляет новое сообщение в список сообщений
def append_message(message):
    # Создаем HTML-элемент представляющий сообщение
    item = document.createElement("li")  # li - это HTML-тег для элемента списка
    item.className = "list-group-item"   # className - определяет как элемент выглядит
    # Добавляем его в список сообщений (chat_window)
    item.innerHTML = f'[<b>{message["sender"]}</b>]: <span>{message["text"]}</span><span class="badge text-bg-light text-secondary">{message["time"]}</span>'
    chat_window.prepend(item)

# Вызывается при клике на send_message
async def send_message_click(e):
    # Отправляем запрос
    sender_full_name = emoji_selector.value + sender.value
    await fetch(f"/send_message?sender={sender_full_name}&text={message_text.value}", method="GET")
    # Очищаем поле
    message_text.value = ""


# Загружает новые сообщения с сервера и отображает их
async def load_fresh_messages():
    global last_seen_id
    # 1 БЫЛО. Загружать все сообщения каждую секунду (большой трафик)
    # 2 СТАЛО. Загружать только новые сообщения
    result = await fetch(f"/get_messages?after={last_seen_id}", method="GET")  # Делаем запрос
    # chat_window.innerHTML = ""  # Очищаем окно с сообщениями
    data = await result.json()
    all_messages = data["messages"]  # Берем список сообщений из ответа сервера
    for msg in all_messages:
        last_seen_id = msg["msg_id"]  # msg_id Последнего сообщение
        append_message(msg)
    set_timeout(1, load_fresh_messages) # Запускаем загрузку заново через секунду


async def message_keypress(event):
    # console.log(event) # Посмотреть нажатие клавишь  - это для отладки
    # вконсоли браузера
    # event.keyCode
    if event.code == 'Enter' or event.code == 'NumpadEnter':
        await send_message_click(event)


# Устнаваливаем действие при клике
send_message.onclick = send_message_click
# Устанавливаем действие при нажатии клавиши
message_text.onkeypress = message_keypress
append_message({"sender":"КИТ", "text":"Пирвет всем участникам чата!!!", "time": "88:88"})
load_fresh_messages()