try:
	import telebot, requests, os
	from telebot import types
	from time import sleep
	from selenium import webdriver

	bot = telebot.TeleBot('1773087186:AAGK6NGqdMCafNraCvR3KmWx9-y_wNonj6c')

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton('старт')

	kk = False
	k = False

	def nak(nl):
		global kk
		global k
		chrome_options = webdriver.ChromeOptions()
		chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--disable-dev-shm-usage")
		chrome_options.add_argument("--no-sandbox")
		browser = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)

		browser.implicitly_wait(5)
		browser.get('https://www.instagram.com/')

		username_input = browser.find_element_by_css_selector("input[name='username']")
		password_input = browser.find_element_by_css_selector("input[name='password']")

		username_input.send_keys(str(kk))
		password_input.send_keys(str(k))

		login_button = browser.find_element_by_css_selector("button[type='submit']")
		login_button.click()
		sleep(5)
		dd = 0

		while True:
			if dd < 3:
				a = requests.post('https://wiq.ru/api/', params={'key': '1356536ce1fe797f8e1ff1b092ef60fe', 'appkey': 'JKnb32hyub', 'action': 'task_start', 'provider': 'insta', 'type': 'follow_profile', 
					'cat': '3', 'login': str(kk)})
				browser.get(a.json()['url'])
				try:
					vfg = browser.find_element_by_css_selector("button[class='_5f5mN       jIbKX  _6VtSN     yZn4P   ']")
					vfg.click()
				except:
					pass
				sleep(.4)
				b = requests.post('https://wiq.ru/api/', params={'key': '1356536ce1fe797f8e1ff1b092ef60fe', 'appkey': 'JKnb32hyub','action': 'task_check', 'id': a.json()['id'], 'login': str(kk)})
				if str(b.json()) == "{'status': True}":
					pass
				else:
					dd+=1
			else:
				bot.send_message(nl, f"Запущено!", reply_markup=markup)
				break



	@bot.message_handler()
	def get_text_messages(message):
	    global kk
	    global k
	    admin = 1455683626    
	    messages = message.from_user.id
	    mess = message.text.lower()
	    if mess == "/start":
	        bot.send_message(messages, f"Привет! \nРады видеть тебя в нашей группе 😊", reply_markup=markup)
	    elif mess == 'cтарт' and kk != False and k != False:
	        bot.send_message(messages, f"Запущено!", reply_markup=markup)
	        nak(messages)
	    elif mess[0:3] == 'лог':
	        kk = str(mess[4:])
	        bot.send_message(messages, f"Готово", reply_markup=markup)
	    elif mess[0:3] == 'пар':
	        k = str(mess[3:])
	        bot.send_message(messages, f"Готово", reply_markup=markup)
	    elif mess == 'дан':
	        bot.send_message(messages,f'{kk} {k}', reply_markup=markup)

	bot.polling(none_stop=True, interval=0)
except:
	os.system('python bot.py')
