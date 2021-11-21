try:
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
		authorize.method('messages.send', {'user_id': sender, 'message': message, "attachment": "audio574170405_456239051,audio574170405_456239053,audio574170405_456239054,audio574170405_456239055", "random_id": get_random_id(),
						   'keyboard': clava3.get_keyboard()})
	    if i == 3:
		authorize.method('messages.send', {'user_id': sender, 'message': message,"random_id": get_random_id(),
						   'keyboard': clava4.get_keyboard()})

	def new_polz(send):
	    # Добавление записи
	    cur.execute(f"SELECT bal FROM tab WHERE id = '{send}'")
	    if str(cur.fetchall()) == '[]':
		cur.execute(f"""INSERT INTO tab (id, bal, clava) VALUES ({send}, 0, 0);""")
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
	    global bal
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

	def pran(send, zn):
	    global roz
	    cur.execute(f"""UPDATE tab SET clava = {int(zn)} WHERE id = {send}""")
	    con.commit()
	    roz = zn
	def clava(send):
	    global i
	    cur.execute(f"SELECT clava FROM tab WHERE id = '{send}'")
	    i = cur.fetchall()[0][0]
	def balans(send):
	    global bal
	    cur.execute(f"SELECT bal FROM tab WHERE id = '{send}'")
	    bal = cur.fetchall()[0][0]
	def prank(send):
	    global roz
	    cur.execute(f"SELECT rozg FROM tab WHERE id = '{send}'")
	    roz = cur.fetchall()[0][0]


	token = "57472ab3e22c6402eae9ab38f55df784f8ec8063c15afff4763089e31dd931591f16455dad565630d36e2"
	authorize = vk_api.VkApi(token=token)
	longpoll = VkLongPoll(authorize)
	admin = 685062634
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
		    balans(sender)
		    write_message(sender, "Твой баланс: " + str(bal) + " руб.")
		elif reseived_message == '№1' and i == 2:
		    pran(sender, 1)
		    clava_n(sender, 3)
		    write_message(sender, 'Введите номер: \nПример: 79283335577')
		elif reseived_message == '№2' and i == 2:
		    pran(sender, 2)
		    clava_n(sender, 3)
		    write_message(sender, 'Введите номер: \nПример: 79283335577')
		elif reseived_message == '№3' and i == 2:
		    pran(sender, 3)
		    clava_n(sender, 3)
		    write_message(sender, 'Введите номер: \nПример: 79283335577')
		elif reseived_message == '№4' and i == 2:
		    pran(sender, 4)
		    clava_n(sender, 3)
		    write_message(sender, 'Введите номер: \nПример: 79283335577')
		elif reseived_message[0:2] == "79" and len(reseived_message) == 11 and i == 3:
		    balans(sender)
		    prank(sender)
		    if bal >= 5:
			if roz == 1:
			    tem = 'Увела друга'
			if roz == 2:
			    tem = 'Гобник'
			if roz == 3:
			    tem = 'Человека'
			if roz == 4:
			    tem = 'Возмущение'
			obnova(sender, 5, 2)
			write_message(admin, f'Номер: {reseived_message} \nТема: {roz}')
			write_message(sender, f'Номер: {reseived_message} \nЗвонок отправлен 😇')
		    else:
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
		    if sender == admin:
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
		    if sender == admin:
			m = extract_arg(event.text)
			t = threading.Thread(target=ras, args=(m,))
			t.start()
			write_message(sender, 'Запущено!')
		    else:
			write_message(sender, 'Вы не админ!')
		else:
		    write_message(sender, 'Не верное действие!')
except:
	os.system('python bot.py')
