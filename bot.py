try:
    import telebot, time, threading, requests, os, psycopg2, random
    from telebot import types

    bot = telebot.TeleBot('5244394682:AAGEJ8axrdH_6KACMbgI-pHnr00fG_ycQbg')
    print('Работает!')
    con = psycopg2.connect(
      database="d1ltclfr932ha7", 
      user="auzmewcyedzwhb", 
      password="6fc7a6f629ce97e31caa99c5560ad0e1d135187a2c88572027bd0eb4b622d642", 
      host="ec2-52-214-125-106.eu-west-1.compute.amazonaws.com", 
      port="5432"
    )
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tab(
        id BIGINT,
        bal BIGINT,
        clava INT,
        ban INT,
        ctavka BIGINT,
        cyma BIGINT,
        ob_sum BIGINT,
        id_stav BIGINT);''')
    con.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS spis(
        cym BIGINT,
        id BIGINT,
        id_stav BIGINT,
        nik TEXT);''')
    con.commit()

    cur.execute('''CREATE TABLE IF NOT EXISTS qiwi(
        popo BIGINT);''')
    con.commit() 

    c1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Играть 🎲')
    item14 = types.KeyboardButton('Профиль 👤')
    item15 = types.KeyboardButton('Баланс 💰')
    item16 = types.KeyboardButton('Пополнить 💳')
    item17 = types.KeyboardButton('Вывод 💸')
    c1.add(item1, item14)
    c1.add(item15, item16)
    c1.add(item17)


    c122 = types.KeyboardButton('Назад ↩')

    nazad = types.ReplyKeyboardMarkup(resize_keyboard=True)
    nazad.add(c122)

    c12 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item12 = types.KeyboardButton('Все ставки 🍀️')
    item142 = types.KeyboardButton('Сделать ставку ♠️')
    c12.add(item12, item142)
    c12.add(c122)

    c13 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    w1 = types.KeyboardButton('5')
    w2 = types.KeyboardButton('10')
    w4 = types.KeyboardButton('20')
    w6 = types.KeyboardButton('30')
    w8 = types.KeyboardButton('40')
    w10 = types.KeyboardButton('50')
    c13.add(w1, w2, w4)
    c13.add(w6, w8, w10)
    c13.add(c122)

    clava2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    c11 = types.KeyboardButton('Оплата Qiwi 🥝')
    c11f = types.KeyboardButton('Оплата Картой 💳')
    c116 = types.KeyboardButton('Проверить оплату.')
    clava2.add(c11)
    clava2.add(c116)
    clava2.add(c116)
    clava2.add(c122)

    ic1 = types.InlineKeyboardMarkup(row_width=2)
    tt = types.InlineKeyboardButton('Пополнить.', callback_data='1')
    tt2 = types.InlineKeyboardButton('Вывод.', callback_data='2')
    ic1.add(tt, tt2)

    ic2 = types.InlineKeyboardMarkup(row_width=2)
    tt2 = types.InlineKeyboardButton('Отменить.', callback_data='ctav')
    ic2.add(tt2)


    def extract_aarg(aarg):
        return aarg.split()[0]


    def extract_arg(arg):
        return arg.split()[1]


    def extract_arg2(arg2):
        return arg2.split()[2]

    def clava(send, zn):
        cur.execute(f"""UPDATE tab SET clava = {zn} WHERE id = {send}""")
        con.commit()

    def obnova(send, cym, zn):
        cur.execute(f"SELECT bal FROM tab WHERE id = '{send}'")
        if zn == 1:
            opop = int(cur.fetchall()[0][0]) + int(cym)
        else:
            opop = int(cur.fetchall()[0][0]) - int(cym)
        # Обнова
        cur.execute(f"""UPDATE tab SET bal = {opop} WHERE id = {send}""")
        con.commit() 

    def obnova2(send, cym):
        cur.execute(f"SELECT ob_sum FROM tab WHERE id = '{send}'")
        opop = int(cur.fetchall()[0][0]) + int(cym)
        # Обнова
        cur.execute(f"""UPDATE tab SET ob_sum = {opop} WHERE id = {send}""")
        con.commit() 

    def obnova3(send):
        cur.execute(f"SELECT id_stav FROM tab WHERE id = '{send}'")
        opop = int(cur.fetchall()[0][0]) + int(1)
        # Обнова
        cur.execute(f"""UPDATE tab SET id_stav = {opop} WHERE id = {send}""")
        con.commit() 

    def sms1(messs, smm, clava):
        bot.send_message(messs, smm, reply_markup=clava)
    def sms(messs, smm):
        bot.send_message(messs, smm)

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
    api_access_token = '5fec7a63ea890c52a6124fcad3d5636d'


    def QiwiCheck(number, api, sender):
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
                    cur.execute(f"""UPDATE qiwi SET popo = {txnId} WHERE popo = {lastpay}""")
                    con.commit()
                    obnova2(comm[3:], sum)
                    sms(int(comm[3:]), "На ваш баланс зачисленно " + str(sum) + " руб.\n\nУдачных игр!")
                except:
                    sms(sender, 'Оплаты нет. ⛔')
        except:
            sms(sender, 'Оплаты нет. ⛔')

    def ras(text):
        # Рaссылка
        cur.execute("SELECT * FROM tab")
        for it in cur.fetchall():
            succes = 0
            fail = 0
            try:
                sms(str(it[0]), str(text))
                succes +=1
            except:
                fail +=1
        sms(admin, "Рассылку получило - " + str(succes) + " пользователей")
        sms(admin, "Заблокировали бота - " + str(fail) + " пользователей")

    @bot.message_handler()
    def get_text_messages(message):
        admin = 5073415776
        sender = message.chat.id
        mess = message.text.lower()
        try:
            cur.execute(f"SELECT * FROM tab WHERE id = '{sender}'")
            infa = cur.fetchall()[0]
            ban = infa[3]
            i = infa[2]
        except:
            if str(cur.fetchall()) == '[]':
                cur.execute(f"""INSERT INTO tab (id, bal, clava, ban, ctavka, cyma, ob_sum, id_stav) VALUES ({sender}, 0, 1, 1, 0, 0, 0, 0);""")
                con.commit()
                ban = 1
                i = 1
                sms1(sender, f'Привет, {message.from_user.first_name}! 😊 \nЖелаем вам больших выигрышей ', c1)
            else:
                pass

        if ban == 0:
            sms(sender, 'Ваш аккаунт заблокирован. ⛔')

        elif mess[0:4] == 'инфа' and sender == admin:
            cur.execute("SELECT id FROM tab")
            jklj = cur.fetchall()
            sms(sender, f'Всего: {len(jklj)} человек.')
        elif mess[0:8] == "рассылка":
            if sender == admin:
                m = message.text[9:]
                t = threading.Thread(target=ras, args=(m,))
                t.start()
                sms(sender, 'Рассылка запущена.')
            else:
                sms(sender, 'Вы не являетесь администратором 👤')

        elif mess[0:14] == 'сделать ставку' and i == 3:
            cur.execute(f"SELECT ctavka FROM tab WHERE id = '{sender}'")
            cy = cur.fetchall()
            ctav = cy[0][0]
            if ctav == 0:
                clava(sender, 4)
                sms1(sender, 'Ставка от 5р до 50р. \nВведите сумму ставки:', c13)
            else:
                cur.execute(f"SELECT * FROM spis WHERE id = '{sender}'")
                cy6 = cur.fetchall()
                ctav6 = cy6[0][0]
                sms1(sender, f'У вас уже есть ставка. 🎲\nСумма: {ctav6} руб. 💰 \nХотите отменить?', ic2)
        elif mess[0:16] == 'проверить оплату' and i == 2:
            clava(sender, 1)
            sms1(sender, 'Проверяем оплату...', c1)
            Tqiwi = threading.Thread(target=QiwiCheck, args=(mylogin, api_access_token, sender))
            Tqiwi.start()
        elif mess[0:6] == 'играть' and i == 1:
            clava(sender, 3)
            sms1(sender, 'Выберите:', c12)
        elif mess[0:13] == 'оплата картой':
            sms(sender, f'Ваш ID: {sender} \nДля оплаты картой пишите:\n@nakrut_ca')
        elif mess[0:3] == 'бан':
            try:
                helovek = extract_arg(mess)
                cur.execute(f"""UPDATE tab SET ban = 0 WHERE id = {helovek}""")
                con.commit() 
                sms(helovek, 'Ваш аккаунт заблокирован. ⛔')
                sms(sender, 'Аккаунт заблокирован. 😇')
            except:
                sms(sender, 'Неверный ID. ⛔')

        elif mess[0:10] == 'все ставки' and i == 3:
            cur.execute("SELECT * FROM spis")
            j = cur.fetchall()
            ooo = 0
            yuyu = []
            for yyy in j:
                if ooo < 6:
                    ooo+=1
                    igra = types.InlineKeyboardMarkup(row_width=3)
                    hjhj = types.InlineKeyboardButton(f'Играть.', callback_data=f'{yyy[2]}:{yyy[1]}')
                    igra.add(hjhj)
                    sms1(sender, f'Игрок: {yyy[3]}\nСтавка: {yyy[0]} руб.', igra)
            if ooo == 0:
                sms(sender, 'Пока ставок нет ☹')

        elif mess[0:5] == 'вывод':
            clava(sender, 10)
            sms1(sender, 'Введите номер Qiwi \nИ сумму вывода 💸 \nПример: \n+79283335522 50 \n+77074470707 75 \n+380443777355 100 \n+375297556655 150 \nКомиссия за вывод 20 - %', nazad)


        elif mess[0:6] == 'разбан':
            try:
                helovek = extract_arg(mess)
                cur.execute(f"""UPDATE tab SET ban = 1 WHERE id = {helovek}""")
                con.commit() 
                sms(helovek, 'Ваш аккаунт разблокирован. 😇')
                sms(sender, 'Аккаунт разблокирован. 😇')
            except:
                sms(sender, 'Неверный ID. ⛔')

        elif mess[0:7] == 'профиль':
            cur.execute(f"SELECT ob_sum FROM tab WHERE id = '{sender}'")
            cy = cur.fetchall()
            ob_sum = int(cy[0][0])
            if ob_sum >= 0 and ob_sum < 10:
                yrov = 'Новичёк.'
            elif ob_sum > 10 and ob_sum <50:
                yrov = 'Средне-слабый.'
            elif ob_sum >= 50 and ob_sum <100:
                yrov = 'Средний.'
            elif ob_sum >= 100 and ob_sum <200:
                yrov = 'Средне-сильный.'
            elif ob_sum >= 200:
                yrov = 'Сильный.'
            bot.send_message(sender, f'👤 ID: `{sender}` \n♦ Уровень: {yrov}\n💰 Общая сумма по-ний: {ob_sum} руб.', parse_mode='Markdown')

        elif mess[0:5] == 'назад' and i == 2 or mess[0:5] == 'назад' and i == 3 or mess[0:5] == 'назад' and i == 10:
            clava(sender, 1)
            sms1(sender, 'Выберите:', c1)
        elif mess[0:5] == 'назад' and i == 4:
            clava(sender, 3)
            sms1(sender, 'Выберите:', c12)

        elif mess[0:6] == "баланс":
            cur.execute(f"SELECT bal FROM tab WHERE id = '{sender}'")
            cy = cur.fetchall()
            bal2 = cy[0][0]
            sms1(sender, "Твой баланс: " + str(bal2) + " руб. 💰", ic1)

        elif mess[0:9] == 'пополнить':
            clava(sender, 2)
            sms1(sender, "Выберите способ оплаты:", clava2)

        elif mess[0:2] == "фф":
            if sender == admin:
                try:
                    id = extract_arg(mess)
                    bal = extract_arg2(mess)
                    obnova(id, bal, 1)
                    obnova2(sender, bal)
                    sms(sender, "Готово.")
                    sms(str(id), "На ваш баланс зачислено " + str(bal) + " руб.")
                except:
                    sms(sender, "Вы не указали айди или сумму.")
            else:
                sms(sender, 'Вы не являетесь администратором 👤')

        elif mess[0:11] == "оплата qiwi" and i == 2:
            clava(sender, 2)
            sms1(sender, 'Кошелек для платежа: +79283692011 \n Примечание к платежу: ' + "1" + str(
                sender) + f' ❗ \n\nТак же оплатить можно с помощью карты (выбирается на сайте). \n\nПосле оплаты на Ваш баланс будет зачислена сумма перевода. Об этом вас уведомят.\n\nhttps://qiwi.com/payment/form/99?extra[%27account%27]=79283692011&amountInteger=1&extra[%27comment%27]=777{sender}&blocked[0]=comment&blocked[1]=account', clava2)
        elif i == 10:
            try:
                deen = extract_aarg(mess)      
                den = extract_arg(mess)
                cur.execute(f"SELECT bal FROM tab WHERE id = '{sender}'")
                cy = cur.fetchall()
                bal2 = cy[0][0]
                if bal2 >= int(den):
                    if int(den) >= 20:
                        obnova(sender, den, 2)
                        clava(sender, 1)
                        sms1(sender, 'Ожидайте вывод в течении \n24-часов 💸', c1)
                        sms(admin, f"Новый вывод 💸 \nID: {sender} \nНомер: {deen} \nСумма: {den}")
                    else:
                        clava(sender, 1)
                        sms1(sender, 'Мин. сумма вывода: 20 руб. ❗', c1)
                else:
                    clava(sender, 1)
                    sms1(sender, 'На вашем балансе недостаточно средств ⛔', c1)
            except:
                clava(sender, 1)
                sms1(sender, 'Неверные данные ⛔', c1)
        elif i == 4:
            try:
                if int(mess) >= 5:
                    if int(mess) <= 50:
                        cur.execute(f"SELECT bal FROM tab WHERE id = '{sender}'")
                        cy = cur.fetchall()
                        bal2 = cy[0][0]
                        if bal2 >= int(mess):
                            obnova3(sender)
                            cur.execute(f"SELECT id_stav FROM tab WHERE id = '{sender}'")
                            cyy = cur.fetchall()
                            id_st = cyy[0][0]
                            obnova(sender, int(mess), 2)
                            cur.execute(f"""INSERT INTO spis (cym, id, id_stav, nik) VALUES ({int(mess)}, {sender}, {id_st}, '{message.from_user.first_name}');""")
                            con.commit()
                            cur.execute(f"""UPDATE tab SET ctavka = 1 WHERE id = {sender}""")
                            con.commit() 
                            clava(sender, 3)
                            sms1(sender, f'Ставка принята ✅\nСумма: {int(mess)} руб. 💰', c12)
                        else:
                            clava(sender, 2)
                            sms1(sender, 'Недостаточно средств ⛔', clava2)
                    else:
                        sms(sender, 'Не более 50 руб ❗')
                else:
                    sms(sender, 'Не менее 5 руб ❗')
            except:
                sms(sender, 'Введите число ❗')


    @bot.callback_query_handler(func=lambda call:True)
    def callback(call):
        if call.message:
            kl5 = 0
            cur.execute("SELECT * FROM spis")
            mm = cur.fetchall()
            for oo in mm:
                if call.data == f'{oo[2]}:{oo[1]}':
                    kl5 = 1
                    cur.execute(f"SELECT bal FROM tab WHERE id = '{call.message.chat.id}'")
                    cy = cur.fetchall()
                    bal2 = cy[0][0]
                    if bal2 >= int(oo[0]):
                        cur.execute(f"DELETE FROM spis WHERE id = {oo[1]};")
                        con.commit()
                        obnova(call.message.chat.id, oo[0], 2)
                        fgfg = random.randint(1, 2)
                        if fgfg == 1:
                            obnova(call.message.chat.id, int(oo[0] * 2), 1)
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= "Выигрыш: " + str(int(oo[0] * 2)) + " руб. 💰")
                            sms(oo[1], 'Ваша ставка проиграна ☹')
                        else:
                            obnova(oo[1], int(oo[0] * 2), 1)
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= "Ваша ставка проиграна ☹")
                            sms(oo[1], f"Выигрыш: " + str(int(oo[0] * 2)) + " руб. 💰")
                        cur.execute(f"""UPDATE tab SET ctavka = 0 WHERE id = {oo[1]}""")
                        con.commit()
                    else:
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= "Недостаточно средств ⛔")





            if call.data == '1':
                clava(call.message.chat.id, 2)
                cur.execute(f"SELECT bal FROM tab WHERE id = '{call.message.chat.id}'")
                cy = cur.fetchall()
                bal2 = cy[0][0]
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= "Твой баланс: " + str(bal2) + " руб. 💰")
                sms1(call.message.chat.id, "Выберите способ оплаты:", clava2)
            elif call.data == '2':
                clava(call.message.chat.id, 10)
                cur.execute(f"SELECT bal FROM tab WHERE id = '{call.message.chat.id}'")
                cy = cur.fetchall()
                bal2 = cy[0][0]
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= "Твой баланс: " + str(bal2) + " руб. 💰")
                sms1(call.message.chat.id, "Введите номер Qiwi \nИ сумму вывода 💸 \nПример: \n+79283335522 50 \n+77074470707 75 \n+380443777355 100 \n+375297556655 150 \nКомиссия за вывод 20 - %", nazad)

            elif call.data == 'ctav':
                cur.execute(f"SELECT * FROM tab WHERE id = '{call.message.chat.id}'")
                cyy = cur.fetchall()
                ctan = cyy[0][4]
                ctid = cyy[0][7]
                if ctan == 1:
                    cur.execute(f"SELECT * FROM spis WHERE id = '{call.message.chat.id}'")
                    u8 = cur.fetchall()
                    try:
                        if ctid == u8[0][2]:
                            cur.execute(f"DELETE FROM spis WHERE id = {call.message.chat.id};")
                            con.commit()
                            obnova(call.message.chat.id, u8[0][0], 1)
                            obnova3(call.message.chat.id)
                            cur.execute(f"""UPDATE tab SET ctavka = 0 WHERE id = {call.message.chat.id}""")
                            con.commit()
                            clava(call.message.chat.id, 3)
                            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f'Возврвт: {u8[0][0]} руб. 💰')
                    except:
                        clava(call.message.chat.id, 3)
                        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='Ставки не существует ⛔ \nВозможно она уже сыграна.')
                else:
                    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text='У вас нет ставок ⛔ \nВозможно она уже сыграна.')
            elif kl5 == 0:
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text= 'Ставки не существует ⛔ \nВозможно она уже сыграна.')


    bot.polling()
except:
    os.system('python bot.py')
