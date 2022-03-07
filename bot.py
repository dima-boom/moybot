try:
    import vk_api, time, threading, psycopg2, os
    from vk_api.longpoll import VkLongPoll, VkEventType
    from vk_api.utils import get_random_id
    from vk_api.keyboard import VkKeyboard, VkKeyboardColor


    con = psycopg2.connect(
      database="d2cqe8nnlid8b9", 
      user="dpfuhmetpzayzs", 
      password="edff53c789ab7de29802257b4912c70343bba33a3ead06b37d1dbe8d48bc4918", 
      host="ec2-176-34-105-15.eu-west-1.compute.amazonaws.com", 
      port="5432"
    )
    cur = con.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS tab(
        id BIGINT,
        clava INT);''')
    con.commit()

    def extract_arg(arg):
        return arg.split()[1]


    def extract_arg2(arg2):
        return arg2.split()[2]

    print("Бот запущен!")
    keyboard = VkKeyboard(one_time=False)
    # 1
    keyboard.add_button('Заказать звонок специалиста', color=VkKeyboardColor.POSITIVE)
    keyboard.add_line()
    keyboard.add_button('Оставить заявку', color=VkKeyboardColor.PRIMARY)
    clava2 = VkKeyboard(one_time=False)
    clava2.add_button('Отмена.', color=VkKeyboardColor.PRIMARY)

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
        write_message(admin, "Рассылку получило - " + str(succes) + " пользователей")
        write_message(admin, "Заблокировали бота - " + str(fail) + " пользователей")

    def clava(send, zn):
        cur.execute(f"""UPDATE tab SET clava = {zn} WHERE id = {send}""")
        con.commit()
    spis = ['а', 'б', 'в', 'г', 'д', 'е', 'ё', 'ж', 'з', 'и', 'й', 'к', 'л', 'м', 'н', 'о', 'п', 'р', 'с', 'т', 'у', 'ф', 'х', 'ц', 'ч', 'ш', 'щ', 'ъ', 'ы', 'ь', 'э', 'ю', 'я']
    token = "a2062453544bfa453c875d3924cd3588b503221eea34aff96431c230e7f8315a950bde7b227c61cd0f352"
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
                user = authorize.method("users.get", {"user_ids": event.user_id})  # вместо 1 подставляете айди нужного юзера
                name = user[0]['first_name']
                write_message(sender, "Привет, " + name + '! \nИспользуй кнопки.')
            elif reseived_message == 'заказать звонок специалиста' and i != 2:
                clava(sender, 2)
                write_message(sender, 'Введите свой номер телефона:')
            elif reseived_message == 'оставить заявку' and i != 3:
                clava(sender, 3)
                write_message(sender, 'Опишите спектр услуг которые вы хотите заказать:')
            elif i == 2:
                d=0
                for m in spis:
                    if m in reseived_message:
                        write_message(sender, 'Неверный номер!')
                        d = 1
                        break
                        
                if d == 1:
                    continue
                if len(reseived_message) > 30:
                    write_message(sender, 'Неверный номер!')
                elif len(reseived_message) < 8:
                    write_message(sender, 'Неверный номер!')
                else:
                    clava(sender, 1)
                    write_message(admin, f'Заказан звонок.\n\n{reseived_message}\n\nСсылка на чат:\nhttps://vk.com/gim211098069?sel={sender}')
                    write_message(sender, 'Номер отправлен, ожидайте.')
            elif i == 3:
                clava(sender, 1)
                write_message(admin, f'Спектр услуг.\n\n{reseived_message}\n\nСсылка на чат:\nhttps://vk.com/gim211098069?sel={sender}')
                write_message(sender, 'Ожидайте ответ.')
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
except:
  os.system('python bot.py')
