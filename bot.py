import vk_api, pywwf, os, time, random, telebot, requests as r
from termcolor import colored
from sys import platform

bot = telebot.TeleBot("1736495852:AAFrs4OON5l06joK25FE5wh8-LBbHI7GdiA")

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
item1 = types.KeyboardButton('старт')
markup.add(item1)

k = 0
kk = 0
kkk = 0

def nak(token, group_col, text):
	vk_session = vk_api.VkApi(token=token)
	vk = vk_session.get_api()


	clear()
	while True:
		try:
			first_group = vk.groups.create(title="Ремонт авто "+str(random.randint(1000, 9999)))["id"]-group_col
			break
		except:
			pass
	clear()
	print(colored("Собираю информацию о "+str(group_col)+" групп...", "cyan"))
	sp_group = []
	itog = []
	grp = first_group
	for i in range(group_col//500):
		sp_group = []
		for k in range(500):
			sp_group.append(str(grp))
			grp+=1
		new_sp = vk.groups.getById(group_ids=sp_group, fields="can_message")
		for j in new_sp:
			if j["can_message"] == 1:
				itog.append(int(j['id']))
			else:
				continue



	clear()
	print(colored("Доступно для рассылки - "+str(len(itog))+" групп\n\n", "cyan"))
	col = 0
	success = 0
	fail = 0
	for D in itog:
		try:
			vk.messages.send(peer_id=-D, random_id=0, message=text)
			print(colored("ID", "blue"), colored(str(D), "magenta"), colored("SUCCES", "green"))
			success += 1
			col += 1
		except KeyboardInterrupt:
			clear()
			print(colored("Вы остановили рассылку", "cyan"))
			break
		except:
			print('cap')
			input()
		try:
			if interval != 0:
				time.sleep(interval)
		except KeyboardInterrupt:
			clear()
			print(colored("Вы остановили рассылку", "cyan"))
			break
	print(colored("\nОтчёт:", "magenta"))
	print(colored("Успешно - "+str(success), "green"), colored("\nНеудачно - "+str(fail), "red"))
	print(colored("Всего отправлено - "+str(col-1), "cyan"))


@bot.message_handler()
def get_text_messages(message):
    global kk
    global k
    global kkk
    admin = 1455683626    
    messages = message.from_user.id
    mess = message.text.lower()
    if mess == "/start":
        bot.send_message(messages, f"Привет! \nРады видеть тебя в нашей группе 😊", reply_markup=markup)
    elif mess == 'cтарт' and kk != 0 and k != 0 and kkk != 0:
        bot.send_message(messages, f"Запущено!", reply_markup=markup)
        nak(messages)
    elif mess[0:3] == 'ток':
        kk = str(mess[4:])
        bot.send_message(messages, f"Готово", reply_markup=markup)
    elif mess[0:5] == 'текст':
        k = str(mess[3:])
        bot.send_message(messages, f"Готово", reply_markup=markup)
    elif mess[0:3] == 'кол':
        k = str(mess[3:])
        bot.send_message(messages, f"Готово", reply_markup=markup)
    elif mess == 'дан':
    	kkk = str(mess[3:])
        bot.send_message(messages,f'{kk} {k}', reply_markup=markup)

bot.polling(none_stop=True, interval=0)
