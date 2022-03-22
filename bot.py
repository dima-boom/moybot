try:
    import telebot, time, threading, requests, os, psycopg2
    from telebot import types

    print('Работает!')
    # Подключение к базе
    con = psycopg2.connect(
      database="dbrqsu9lrjaedd", 
      user="golstwfzgimtjb", 
      password="721335c79988e6b4ee638deaa85dc0e49bff1d8ab7fd77ddd070521362c4d07b", 
      host="ec2-99-80-170-190.eu-west-1.compute.amazonaws.com", 
      port="5432"
    )

    cur = con.cursor() 
    # Основная таблица
    cur.execute('''CREATE TABLE IF NOT EXISTS tab(
        id BIGINT,
        bal BIGINT,
        clava INT,
        nom_id BIGINT,
        nomer BIGINT,
        pozi INT);''')
    con.commit()

    # Qiwi таблица
    cur.execute('''CREATE TABLE IF NOT EXISTS qiwi(
        popo BIGINT);''')
    con.commit()

    bot = telebot.TeleBot('5209957972:AAHhojlbKE22-Vj8LROsU7xyvjANTR2ODEw') # Токен бота

    c1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # с1_1 = types.KeyboardButton('Русский 🇷🇺')
    # с1_2 = types.KeyboardButton('Индонезия 🇮🇩')
    c1_3 = types.KeyboardButton('USA 🇱🇷')
    # с1.add(с1_1, с1_2)
    c1.add(c1_3)
    c1_3 = types.KeyboardButton('Баланс 💰')
    c1_4 = types.KeyboardButton('Пополнить 💳')
    c1_5 = types.KeyboardButton('Тариф')
    c1_6 = types.KeyboardButton('Правила')
    c1.add(c1_3, c1_4)
    c1.add(c1_5, c1_6)

    c2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    c2_1 = types.KeyboardButton('Оплата Qiwi 🥝')
    c2.add(c2_1)
    c2_2 = types.KeyboardButton('Назад ↩')
    c2.add(c2_2)

    c3 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    c3_1 = types.KeyboardButton('Назад ↩')
    c3.add(c3_1)

    c4 = types.InlineKeyboardMarkup(row_width=1)
    c4_1 = types.InlineKeyboardButton('Проверить СМС ✉', callback_data='sms_status')
    c4_2 = types.InlineKeyboardButton('Отмена ❌', callback_data='sms_otmena')
    c4.add(c4_1, c4_2)

    c5 = types.InlineKeyboardMarkup(row_width=1)
    c5_1 = types.InlineKeyboardButton('Пополнить.', callback_data='bal_popl')
    c5.add(c5_1)

    def extract_aarg(arg):
        return arg.split()[0]

    def extract_arg(arg):
        return arg.split()[1]

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

    mylogin = '79283692011' # Номер qiwi
    api_access_token = 'bdea16d6d7de9b1001fda7d46a6cff7c' # Токен qiwi

    def QiwiCheck(number, api, sender): # Проверка оплаты qiwi
        try:
            lastPayments = payment_history_last(number, api, '1', '', '')
            num = lastPayments['data'][0]['account']
            sum = lastPayments['data'][0]['sum']['amount']
            comm = lastPayments['data'][0]['comment']
            type = lastPayments['data'][0]['type']
            txnId = lastPayments['data'][0]['txnId']
            txnId = str(txnId)

            cur.execute("SELECT * FROM qiwi")
            lastpay = cur.fetchall()[0][0]
            lastpay = str(lastpay)

            if lastpay == txnId:
                sms(sender, 'Оплаты нет. ⛔')
            else:
                try:
                    cur.execute(f"SELECT bal FROM tab WHERE id = '{str(comm[3:])}'")
                    opop = int(cur.fetchall()[0][0]) + int(sum)
                    cur.execute(f"""UPDATE tab SET bal = {opop} WHERE id = {str(comm[3:])}""")
                    con.commit() 
                    cur.execute(f"SELECT ref FROM tab WHERE id = '{str(comm[3:])}'")
                    mkmk = int(cur.fetchall())
                    ttt = int(sum * 0.05)
                    obnova5(mkmk, ttt)
                    cur.execute(f"""UPDATE qiwi SET popo = {txnId} WHERE popo = {lastpay}""")
                    con.commit()
                    obnova2(comm[3:], sum)
                    sms(int(comm[3:]), "На ваш баланс зачисленно " + str(sum) + " руб.\n\nУдачных игр!")
                except:
                    sms(sender, 'Оплаты нет. ⛔')
        except:
            sms(sender, 'Оплаты нет. ⛔')

    # Запуск проверки оплаты qiwi
    # Tqiwi = threading.Thread(target=QiwiCheck, args=(mylogin, api_access_token))
    # Tqiwi.start()

    def ras(text, admin): # Рассылка
        # Рaссылка
        cur.execute("SELECT * FROM tab")
        succes = 0
        fail = 0
        for it in cur.fetchall():
            try:
                sms(str(it[0]), str(text))
                succes +=1
            except:
                fail +=1
        sms(admin, "Рассылку получило - " + str(succes) + " пользователей\nЗаблокировали бота - " + str(fail) + " пользователей")

    def sms1(messs, smm, clava): # Отправка смс с клавиатурой
        bot.send_message(messs, smm, reply_markup=clava)

    def sms(messs, smm): # Отправка смс
        bot.send_message(messs, smm)

    def obnova(send, cym, zn): # Изменения баланса
        cur.execute(f"SELECT bal FROM tab WHERE id = '{send}'")
        if zn == 1:
            opop = int(cur.fetchall()[0][0]) + int(cym)
        else:
            opop = int(cur.fetchall()[0][0]) - int(cym)
        # Обнова
        cur.execute(f"""UPDATE tab SET bal = {opop} WHERE id = {send}""")
        con.commit() 


    def clava(send, zn):
        cur.execute(f"""UPDATE tab SET clava = {zn} WHERE id = {send}""")
        con.commit()

    @bot.message_handler()
    def get_text_messages(message):
        admin = 1455683626 # ID Админа
        id = message.from_user.id # ID Пользователя
        mess = message.text.lower() # Текст сообщения 

        try:
            cur.execute(f"SELECT * FROM tab WHERE id = '{id}'")
            infa = cur.fetchall()[0]
            i = infa[2]
        except:
            lolo = cur.fetchall()
            if str(lolo) == '[]':
                cur.execute(f"""INSERT INTO tab (id, bal, clava, nom_id, nomer, pozi) VALUES ({id}, 0, 1, 0, 0, 0);""")
                con.commit()
                ban = 1
                i = 15
                n=0
                sms1(id, f'Привет, {message.from_user.first_name}! 😊 \nВведите реверальный код:', c1)
            else:
                pass

        if mess == "/start":
            bot.send_message(id, f"Привет {message.from_user.first_name}! \nРады видеть тебя 😊", reply_markup=c1)

        elif mess[0:8] == "рассылка":
            if id == admin:
                m = message.text[9:]
                t = threading.Thread(target=ras, args=(m,))
                t.start()
                sms(id, 'Рассылка запущена.')
            else:
                sms(id, 'Вы не являетесь \nадминистратором 👤')
        elif mess[0:16] == 'проверить оплату' and i == 2:
            clava(sender, 1)
            sms1(sender, 'Проверяем оплату...', c1)
            Tqiwi = threading.Thread(target=QiwiCheck, args=(mylogin, api_access_token, id))
            Tqiwi.start()
        elif mess[0:5] == 'тариф':
            sms(id, 'Номер: USA - 3p.')

        elif mess[0:7] == 'правила':
            sms(id, '1.Номер уже может быть использован, на это нет гарантии!\n\n2.Блокировка аккаунта может быть сразу после его создания.\n\n3.Создание аккаунта нужно делать с использованием VPN сервиса той-же страны номер которой вы используете для его создания.')

        elif mess[0:6] == "баланс":
            cur.execute(f"SELECT bal FROM tab WHERE id = '{id}'")
            cy = cur.fetchall()
            bal2 = cy[0][0]
            sms1(id, "Твой баланс: " + str(bal2) + " руб. 💰", c5)

        elif mess[0:9] == 'пополнить':
            clava(id, 2)
            sms1(id, "Выберите способ оплаты:", c2)

        elif mess[0:2] == "фф":
            if id == admin:
                try:
                    ids = extract_arg(mess)
                    bal = extract_arg2(mess)
                    obnova(ids, bal, 1)
                    sms(id, "Готово.")
                    sms(str(id), "На ваш баланс зачислено " + str(bal) + " руб.")
                except:
                    sms(id, "Вы не указали айди или сумму.")
            else:
                sms(id, 'Вы не являетесь администратором 👤')

        elif mess[0:9] == 'пополнить':
            clava(id, 2)
            sms1(id, "Выберите способ оплаты:", c2)

        elif mess[0:5] == 'назад' and i == 2:
            clava(id, 1)
            sms1(id, 'Выберите:', c1)

        elif mess[0:11] == "оплата qiwi" and i == 2:
            clava(id, 2)
            sms1(id, 'Кошелек для платежа: +79283692011 \n Примечание к платежу: ' + "777" + str(
                id) + f' ❗ \n\nТак же оплатить можно с помощью карты (выбирается на сайте). \n\nПосле оплаты на Ваш баланс будет зачислена сумма перевода. Об этом вас уведомят.\n\nhttps://qiwi.com/payment/form/99?extra[%27account%27]=79283692011&amountInteger=1&extra[%27comment%27]=777{id}&blocked[0]=comment&blocked[1]=account', c2)


        # elif mess[0:7] == 'русский':
        #     b = requests.get('https://sms-acktiwator.ru/api/getnumber/52383f3c6b4cb1e74028b13bca624940cbc15fc8?id=2&code=ID')        post = b.text.split(':')
        #     ids = post[1]
        #     nomer = post[2]

        # elif mess[0:9] == 'индонезия':
        #     b = requests.get('https://sms-acktiwator.ru/api/getnumber/52383f3c6b4cb1e74028b13bca624940cbc15fc8?id=2&code=ID')

        elif mess[0:3] == 'usa':
            cur.execute(f"SELECT * FROM tab WHERE id = '{id}'")
            cy = cur.fetchall()[0]
            if int(cy[5]) == 1:
                cur.execute(f"SELECT * FROM tab WHERE id = '{id}'")
                raxd = cur.fetchall()[0]
                idd = raxd[3]
                nomer = raxd[4]
                bot.send_message(id, f'Вы уже взяли один Номер: \n\n📲 Номер: `+{nomer}`\n♦ ID: `{idd}`\n✉ SMS-Code: Ожидание..', reply_markup=c4, parse_mode='Markdown')
            else:
                bal2 = cy[1]
                if int(bal2) >= 3:
                    obnova(id, 3, 2)
                    cur.execute(f"""UPDATE tab SET pozi = 1 WHERE id = {id}""")
                    con.commit() 
                    b = requests.get(f'https://sms-code.store/stubs/handler_api.php?api_key=598279d2cd5da2a7d08cf4fd0dc497&action=getNumber&service=vk&country=12', verify=False)
                    post = b.text.split(':')
                    idd = post[1]
                    nomer = post[2]
                    cur.execute(f"""UPDATE tab SET nom_id = {idd} WHERE id = {id}""")
                    con.commit()
                    cur.execute(f"""UPDATE tab SET nomer = {nomer} WHERE id = {id}""")
                    con.commit()
                    bot.send_message(id, f'📲 Номер: `+{nomer}`\n♦ ID: `{idd}`\n✉ SMS-Code: Ожидание..', reply_markup=c4, parse_mode='Markdown')
                else:
                    clava(id, 2)
                    sms1(id, 'Недостаточно средств. ⛔', c2)

    @bot.callback_query_handler(func=lambda call:True)
    def callback(call):
        if call.message:
            if call.data == 'sms_status':
                cur.execute(f"SELECT * FROM tab WHERE id = '{call.message.chat.id}'")
                raxd = cur.fetchall()[0]
                idd = raxd[3]
                nomer = raxd[4]
                if int(raxd[5]) == 0:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='❌ Проверять нечего.')
                else:
                    b = requests.get(f'https://sms-code.store/stubs/handler_api.php?api_key=598279d2cd5da2a7d08cf4fd0dc497&action=getStatus&id={idd}', verify=False)
                    if str(b.text.split(':')[0]) == 'STATUS_OK':
                        cod = b.text.split(':')[1]
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Обноваление..')
                        bot.send_message(call.message.chat.id, f'📲 Номер: `+{nomer}`\n♦ ID: `{idd}`\n✉ SMS-Code: `{cod}` ✅', reply_markup=c1, parse_mode='Markdown')
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Обноваление..')
                        bot.send_message(call.message.chat.id, f'📲 Номер: `+{nomer}`\n♦ ID: `{idd}`\n✉ SMS-Code: Ожидание..', reply_markup=c4, parse_mode='Markdown')

            elif call.data == 'sms_otmena':
                cur.execute(f"SELECT * FROM tab WHERE id = '{call.message.chat.id}'")
                raxd = cur.fetchall()[0]
                if int(raxd[5]) == 0:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='❌ Отменять нечего.')
                else:
                    idd = raxd[3]
                    nomer = raxd[4]
                    b = requests.get(f'https://sms-code.store/stubs/handler_api.php?api_key=598279d2cd5da2a7d08cf4fd0dc497&action=getStatus&id={idd}', verify=False)

                    if str(b.text.split(':')[0]) == 'STATUS_OK':
                        cod = b.text.split(':')[1]
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Обноваление..')
                        bot.send_message(call.message.chat.id, f'📲 Номер: +`{nomer}`\n♦ ID: `{idd}`\n✉ SMS-Code: `{cod}` ✅', reply_markup=c1, parse_mode='Markdown')
                    else:
                        obnova(call.message.chat.id, 3, 1)
                        requests.get(f'https://sms-code.store/stubs/handler_api.php?api_key=598279d2cd5da2a7d08cf4fd0dc497&action=setStatus&status=8&id={idd}', verify=False)
                        cur.execute(f"""UPDATE tab SET pozi = 0 WHERE id = {call.message.chat.id}""")
                        con.commit() 
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='❌ Отмена покупки.')
            elif call.data == 'bal_popl':
                clava(call.message.chat.id, 2)
                cur.execute(f"SELECT bal FROM tab WHERE id = '{call.message.chat.id}'")
                cy = cur.fetchall()
                bal2 = cy[0][0]
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= "Твой баланс: " + str(bal2) + " руб. 💰")
                sms1(call.message.chat.id, "Выберите способ оплаты:", c2)

    bot.polling(none_stop=True, interval=0)
except:
  os.system('python bot.py')
