try:
    import vk_api, time, psycopg2, os
    from vk_api.longpoll import VkLongPoll, VkEventType
    from vk_api.utils import get_random_id
    from vk_api.keyboard import VkKeyboard, VkKeyboardColor

    con = psycopg2.connect(
      database="dcqc7uuppskloi", 
      user="jzllnlrkewbtsb", 
      password="3c8b2a70907d80d2f11c60597fa34093a9c5212b210718447b6ad4849a831bb5", 
      host="ec2-99-80-170-190.eu-west-1.compute.amazonaws.com", 
      port="5432"
    )

    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tab(
        id BIGINT,
        clava INT);''')
    con.commit()

    # cur.execute('''CREATE TABLE IF NOT EXISTS qiwi(
    #     popo BIGINT);''')
    #     con.commit()
    #     cur.execute(f"""INSERT INTO qiwi (id, clava) VALUES ({sender}, 1);""")
    #     con.commit()

    def extract_arg(arg):
        return arg.split()[1]

    def extract_arg2(arg2):
        return arg2.split()[2]

    print("Бот запущен!")
    keyboard = VkKeyboard(one_time=False)
    keyboard.add_button('Заказать спам!', color=VkKeyboardColor.POSITIVE)

    clava2 = VkKeyboard(one_time=False)
    clava2.add_button('1', color=VkKeyboardColor.PRIMARY)
    clava2.add_button('2', color=VkKeyboardColor.PRIMARY)
    clava2.add_line()
    clava2.add_button('3', color=VkKeyboardColor.PRIMARY)
    clava2.add_button('4', color=VkKeyboardColor.PRIMARY)
    clava2.add_line()
    clava2.add_button('5', color=VkKeyboardColor.PRIMARY)

    def write_message(sender, message):
        authorize.method('messages.send', {'user_id': sender, 'message': message, "random_id": get_random_id(), 'keyboard': keyboard.get_keyboard()})
    def write_message1(sender, message):
        authorize.method('messages.send', {'user_id': sender, 'message': message, "random_id": get_random_id(), 'keyboard': clava2.get_keyboard()})

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
        write_message(admin, "Рассылку получило - " + str(succes) + " пользователей. \nЗаблокировали бота - " + str(fail) + " пользователей.")

    def clava(send, zn):
        cur.execute(f"""UPDATE tab SET clava = {zn} WHERE id = {send}""")
        con.commit()

    token = "08c55e2e449b9a861ab867e8c421a7dba85b524a34d7b2b77642c1542d4f2070b45cd597768139fd9595d"
    authorize = vk_api.VkApi(token=token)
    longpoll = VkLongPoll(authorize)
    admin = 191475945
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reseived_message = event.text.lower()
            sender = event.user_id
            try:
                cur.execute(f"SELECT * FROM tab WHERE id = '{sender}'")
                i = cur.fetchall()[0][1]
            except:
                lolo = cur.fetchall()
                if str(lolo) == '[]':
                    cur.execute(f"""INSERT INTO tab (id, clava) VALUES ({sender}, 1);""")
                    con.commit()
                    i=1
                else:
                    pass
            if reseived_message == 'начать' \
                    or reseived_message == 'начать' \
                    or reseived_message == 'привет'\
                    or reseived_message == 'ку'\
                    or reseived_message == 'хай' \
                    or reseived_message == 'здравствуйте' \
                    or reseived_message == 'start' \
                    or reseived_message == 'дарова':
                user = authorize.method("users.get", {"user_ids": event.user_id})  
                name = user[0]['first_name']
                write_message(sender, "Привет, " + name + '! \nОтправьте ссылку на жертву.\nПример: https://vk.com/id7777')

            elif reseived_message[0:13] == 'заказать спам':
                write_message(sender, 'Отправьте ссылку на жертву.\nПример: https://vk.com/id7777')

            elif reseived_message[0:15] == 'https://vk.com/' or reseived_message[0:17] == 'https://m.vk.com/' and len(reseived_message) > 20:
                clava(sender, 2)
                write_message1(sender, '100 сообщений - 20 рублей \n200 сообщений - 30 рублей \n500 сообщений - 50 рублей \n750 сообщений - 75 рублей \n1500 сообщений - 100 рублей')

            elif reseived_message == '1' and i == 2:
                clava(sender, 1)
                write_message(sender, f'Оплатите 20р по ссылке. \nОБЯЗАТЕЛЬНО ДОБАВЬТЕ КОММЕНТАРИЙ - {sender}\n\nhttps://donate.qiwi.com/payin/sms?senderName=SMS&message={sender}')

            elif reseived_message == '2' and i == 2:
                clava(sender, 1)
                write_message(sender, f'Оплатите 30р по ссылке. \nОБЯЗАТЕЛЬНО ДОБАВЬТЕ КОММЕНТАРИЙ - {sender}\n\nhttps://donate.qiwi.com/payin/sms?senderName=SMS&message={sender}')

            elif reseived_message == '3' and i == 2:
                clava(sender, 1)
                write_message(sender, f'Оплатите 50р по ссылке. \nОБЯЗАТЕЛЬНО ДОБАВЬТЕ КОММЕНТАРИЙ - {sender}\n\nhttps://donate.qiwi.com/payin/sms?senderName=SMS&message={sender}')

            elif reseived_message == '4' and i == 2:
                clava(sender, 1)
                write_message(sender, f'Оплатите 75р по ссылке. \nОБЯЗАТЕЛЬНО ДОБАВЬТЕ КОММЕНТАРИЙ - {sender}\n\nhttps://donate.qiwi.com/payin/sms?senderName=SMS&message={sender}')

            elif reseived_message == '5' and i == 2:
                clava(sender, 1)
                write_message(sender, f'Оплатите 100р по ссылке. \nОБЯЗАТЕЛЬНО ДОБАВЬТЕ КОММЕНТАРИЙ - {sender}\n\nhttps://donate.qiwi.com/payin/sms?senderName=SMS&message={sender}')


            elif reseived_message[0:8] == "рассылка":
                try:
                    if sender == admin:
                        m = extract_arg(event.text)
                        t = threading.Thread(target=ras, args=(m,))
                        t.start()
                        write_message(sender, 'Запущено!')
                    else:
                        write_message(sender, 'Вы не админ!')
                except:
                    pass
            else:
                if i == 1:
                    write_message(sender, 'Я вас не понял! \nОтправьте ссылку на жертву.\nПример: https://vk.com/id7777')
                elif i == 2:
                    write_message1(sender, 'Я вас не понял! \n100 сообщений - 20 рублей \n200 сообщений - 30 рублей \n500 сообщений - 50 рублей \n750 сообщений - 75 рублей \n1500 сообщений - 100 рублей')
except:
    os.system('python bot.py')
