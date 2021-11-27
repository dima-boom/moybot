import vk_api, requests, time, threading, psycopg2 
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from vk_api.keyboard import VkKeyboard, VkKeyboardColor


con = psycopg2.connect(
  database="d6mk8lfg7oufvn", 
  user="bnrtdzcoblcxja", 
  password="f6fcbdc55d5a6a338627ca3971801af46277eb0f81245b08ca6b3051580c9f28", 
  host="ec2-54-154-101-45.eu-west-1.compute.amazonaws.com", 
  port="5432"
)
cur = con.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS tab(
    id INT,
    bal INT,
    clava INT,
    rozg INT);''')
con.commit()  

cur.execute('''CREATE TABLE IF NOT EXISTS qiwi(
    id INT,
    wiw INT);''')
con.commit()

print("Бот запущен!")
keyboard = VkKeyboard(one_time=False)
# 1
keyboard.add_button('Розыгрыши 🎉', color=VkKeyboardColor.PRIMARY)
keyboard.add_line()
keyboard.add_button('Баланс 💰', color=VkKeyboardColor.PRIMARY)
keyboard.add_button('Пополнить 💳', color=VkKeyboardColor.PRIMARY)

clava2 = VkKeyboard(one_time=False)
clava2.add_button('Оплата Qiwi 🥝', color=VkKeyboardColor.PRIMARY)
clava2.add_line()
clava2.add_button('Назад ↩', color=VkKeyboardColor.SECONDARY)

clava3 = VkKeyboard(one_time=False)
clava3.add_button('№1', color=VkKeyboardColor.SECONDARY)
clava3.add_button('№2', color=VkKeyboardColor.SECONDARY)
clava3.add_line()
clava3.add_button('№3', color=VkKeyboardColor.SECONDARY)
clava3.add_button('№4', color=VkKeyboardColor.SECONDARY)
clava3.add_line()
clava3.add_button('Назад ↩', color=VkKeyboardColor.SECONDARY)

clava4 = VkKeyboard(one_time=False)
clava4.add_button('Назад ↩', color=VkKeyboardColor.SECONDARY)

def extract_arg(arg):
    return arg.split()[1]


def extract_arg2(arg2):
    return arg2.split()[2]

def write_message(sender, message):
    if i == 0:
        authorize.method('messages.send', {'user_id': sender, 'message': message, "random_id": get_random_id(),
                                                   'keyboard': keyboard.get_keyboard()})
    if i == 1:
        authorize.method('messages.send', {'user_id': sender, 'message': message, "random_id": get_random_id(),
                                           'keyboard': clava2.get_keyboard()})
    if i == 2:
        authorize.method('messages.send', {'user_id': sender, 'message': message, "attachment": "audio643773648_456239021,audio643773648_456239020,audio643773648_456239019,audio643773648_456239017", "random_id": get_random_id(),
                                           'keyboard': clava3.get_keyboard()})
    if i == 3:
        authorize.method('messages.send', {'user_id': sender, 'message': message,"random_id": get_random_id(),
                                           'keyboard': clava4.get_keyboard()})

def new_polz(send):
    # Добавление записи
    cur.execute(f"SELECT bal FROM tab WHERE id = '{send}'")
    if str(cur.fetchall()) == '[]':
        cur.execute(f"""INSERT INTO tab (id, bal, clava, rozg) VALUES ({send}, 3, 0, 0);""")
        con.commit()
    else:
        pass
def ras(text):
    # Рaссылка
    cur.execute("SELECT * FROM tab")
    for it in cur.fetchall():
        succes = 0
        fail = 0
        try:
            authorize.method('messages.send', {'user_id': str(it[0]), 'message': str(text), "random_id": get_random_id()})
            succes +=1
        except:
            fail +=1
    write_message(admin, "Рассылку получило - " + str(succes) + " пользователей")
    write_message(admin, "Заблокировали бота - " + str(fail) + " пользователей")
def obnova(send, cym, zn):
    cur.execute(f"SELECT bal FROM tab WHERE id = '{send}'")
    if zn == 1:
        opop = int(cur.fetchall()[0][0]) + int(cym)
    else:
        opop = int(cur.fetchall()[0][0]) - int(cym)
    # Обнова
    cur.execute(f"""UPDATE tab SET bal = {opop} WHERE id = {send}""")
    con.commit() 
def clava_n(send, zn):
    global i
    cur.execute(f"""UPDATE tab SET clava = {int(zn)} WHERE id = {send}""")
    con.commit()
    i = zn

def clava(send):
    global i
    cur.execute(f"SELECT clava FROM tab WHERE id = '{send}'")
    i = cur.fetchall()[0][0]

def payment_history_last(my_login, api_access_token, rows_num, next_TxnId, next_TxnDate):
    # сессия для рекуест
    s = requests.Session()
    # добавляем рекуесту headers
    s.headers['authorization'] = 'Bearer ' + api_access_token
    # параметры
    parameters = {'rows': rows_num, 'nextTxnId': next_TxnId, 'nextTxnDate': next_TxnDate}
    # через рекуест получаем платежы с параметрами - parameters
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params=parameters)
    # обязательно json все объекты в киви апи json
    return h.json()
mylogin = '79283692011'
api_access_token = '17b80073f6c228dde9bf1b3c7f031e4f'

def QiwiCheck(number, api):
    while True:
        time.sleep(30)
        lastPayments = payment_history_last(number, api, '1', '', '')

        num = lastPayments['data'][0]['account']
        sum = lastPayments['data'][0]['sum']['amount']
        comm = lastPayments['data'][0]['comment']
        type = lastPayments['data'][0]['type']
        txnId = lastPayments['data'][0]['txnId']
        txnId = str(txnId)

        cur.execute("SELECT * FROM qiwi")
        lastpay = cur.fetchall()[0][1]

        if str(lastpay) == txnId:
            pass
        else:
            try:
                cur.execute(f"""UPDATE qiwi SET wiw = {int(txnId)} WHERE id = 1""")
                con.commit()
                obnova(int(comm[1:]), int(sum), 1)

                write_message(int(comm[1:]), "На ваш баланс зачислено: " + str(sum) + "р.\n\nУдачных покупок!")

            except:
                pass

Tqiwi = threading.Thread(target=QiwiCheck, args=(mylogin, api_access_token))
Tqiwi.start()


def mmm(phone, id):
    requests.post(f'https://zvonok.com/manager/cabapi_external/api/v1/phones/call/?campaign_id={id}&phone=%2B{phone}&public_key=384f4635b7ea6cdb77b7161ff4614e25')
    while range(5):
        time.sleep(40)
        a = requests.post(f'https://zvonok.com/manager/cabapi_external/api/v1/phones/calls_by_phone/?campaign_id={id}&phone=%2B{phone}&public_key=384f4635b7ea6cdb77b7161ff4614e25')
        if str(a.json()[0]['status_display']) == 'Закончен удачно':
            b = requests.get(str(a.json()[0]['recorded_audio']), stream=True)
            with open(str(phone) + '.mp3', 'wb') as fd:
                fd.write(b.content)
            return


token = "78d498303369d6dffdc3a4636a23d5ae7d2e048c7d3e27c212a3ca8d72c667ec05a83003ad0175babdb38"
authorize = vk_api.VkApi(token=token)
longpoll = VkLongPoll(authorize)
admin = [643773648, 685062634]
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        reseived_message = event.text.lower()
        sender = event.user_id
        new_polz(sender)
        clava(sender)
        if reseived_message == 'начать' \
                or reseived_message == 'начать' \
                or reseived_message == 'привет'\
                or reseived_message == 'ку'\
                or reseived_message == 'хай' \
                or reseived_message == 'здравствуйте' \
                or reseived_message == 'start' \
                or reseived_message == 'дарова':
            user = authorize.method("users.get", {"user_ids": event.user_id})  # вместо 1 подставляете айди нужного юзера
            name = user[0]['first_name']
            write_message(sender, "Привет, " + name + '! \nРады видеть тебя в нашей группе 😊')
            write_message(sender, 'Вы в главном меню: \n\n- Розыгрыши \n- Баланс \n- Пополнить')

        elif reseived_message[0:6] == "баланс":
            cur.execute(f"SELECT bal FROM tab WHERE id = '{sender}'")
            bal = cur.fetchall()[0][0]
            write_message(sender, "Твой баланс: " + str(bal) + " руб.")
        elif reseived_message == '№1' and i == 2 or \
            reseived_message == '№2' and i == 2 or \
            reseived_message == '№3' and i == 2 or \
            reseived_message == '№4' and i == 2:
            hj = int(reseived_message[1:])
            cur.execute(f"""UPDATE tab SET rozg = {hj} WHERE id = {sender}""")
            con.commit()
            clava_n(sender, 3)
            write_message(sender, 'Введите номер: \nПример: 79283335577')
        elif reseived_message[0:2] == "79" and len(reseived_message) == 11 and i == 3:
            cur.execute(f"SELECT * FROM tab WHERE id = '{sender}'")
            cy = cur.fetchall()
            roz = cy[0][3]
            bal = cy[0][1]
            if bal >= 5:
                print(roz)
                if roz == 1:
                    t = threading.Thread(target=mmm, args=(reseived_message, 492017820))
                    t.start()
                elif roz == 2:
                    t = threading.Thread(target=mmm, args=(reseived_message, 842512569))
                    t.start()
                elif roz == 3:
                    t = threading.Thread(target=mmm, args=(reseived_message, 875086153))
                    t.start()
                elif roz == 4:
                    t = threading.Thread(target=mmm, args=(reseived_message, 2130706234))
                    t.start()
                obnova(sender, 5, 2)
                clava_n(sender, 0)
                write_message(sender, f'Номер: {reseived_message} ✅\nЗвонок отправлен 😇')
            else:
                clava_n(sender, 1)
                write_message(sender, 'У вас недостаточно средств :(')
        elif reseived_message[0:9] == "пополнить":
            clava_n(sender, 1)
            write_message(sender, "Выберите способ оплаты:")
        elif reseived_message[0:11] == "оплата qiwi" and i == 1:
                write_message(sender,
                              'Qiwi-кошелёк: +79283692011 \nНе забудьте указать этот код в комментариях к платежу: ' + "1" + str(
                                  sender) + ' ❗ '
                                            '\n\nПосле оплаты на ваш баланс автоматически в течении минуты будет зачисленна сумма перевода, если оплата придет вам сообщат')
        elif reseived_message[0:5] == 'назад' and i == 1 or reseived_message[0:5] == 'назад' and i == 2:
            clava_n(sender, 0)
            write_message(sender, 'Вы в главном меню: \n\n- Розыгрыши \n- Баланс \n- Пополнить')
        elif reseived_message[0:9] == 'розыгрыши':
            clava_n(sender, 2)
            write_message(sender, 'Выберите номер розыгрыша 🎉 \nЦена: 5 руб - 1 звонок ☎')
        elif reseived_message[0:5] == 'назад' and i == 3:
            clava_n(sender, 2)
            write_message(sender, "Выберите номер розыгрыша 🎉")
        elif reseived_message[0:2] == "фф":
            if sender in admin:
                try:
                    id = extract_arg(reseived_message)
                    ball = extract_arg2(reseived_message)
                    obnova(sender, ball, 1)
                    write_message(event.user_id, "Готово")
                    write_message(str(id), "На ваш баланс зачислено " + str(ball) + " руб.")
                except:
                    write_message(event.user_id, "Вы не указали айди или сумму")
            else:
                write_message(sender, 'Вы не являетесь администратором !!!')


        elif reseived_message[0:8] == "рассылка":
            if sender in admin:
                m = extract_arg(event.text)
                t = threading.Thread(target=ras, args=(m,))
                t.start()
                write_message(sender, 'Запущено!')
            else:
                write_message(sender, 'Вы не админ!')
        else:
            if i == 0:
                    write_message(sender, 'Вы в главном меню: \n\n- Розыгрыши \n- Баланс \n- Пополнить')
            elif i == 1:
                write_message(sender, 'Пожалуйста используйте кнопки:')
            elif i == 2:
                write_message(sender, 'Выберите вариант с помощью кнопок:')
            elif i == 3
                write_message(sender, 'Не верно !!! \nВведите номер: \nПример: 79283335577')
