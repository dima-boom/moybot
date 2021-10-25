try:
	import telebot, vk_api, time, requests, os, vk_captchasolver as vc
	from telebot import types
	from time import sleep

	bot = telebot.TeleBot('2095375506:AAH28FwvC00BtCMH5Li6n3QHfBrMw1NvtEk')

	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	item1 = types.KeyboardButton('Старт')
	item2 = types.KeyboardButton('Стоп')
	markup.add(item1)
	markup.add(item2)
	l = 0
	def ferma():
		global l
		kkkk ={'1': {'key': 'b5bcdb00bb7d103e1dc6b4673e5e6a0633bbb251daa9dfd6', 'tok': '896f9cb2e79727aa480cf4ee923680d50af3f8293c8b7ffe1bcdcb8660505fa57a956e45d444d58ef4301'}, 
		    '2': {'key': '639e8ac02e846f31179f8c80e7bc6f738bf1c4d5dee637f4', 'tok': '26fe16d2b5b7c5c888527b26ebac447220c5b19f0ab469eef756318274ebbb19c7f249d924da7621ab8e9'}, 
		    '3': {'key': '43782766326f1c99618c6e33b436d7a1794005459209d6ed', 'tok': 'e70daa7a8b260eadecd3fa17269115aac1212494ae11c8e28c848f78377b94f8084b1c0d7a5d7463eff53'},
		    '4': {'key': '29d2f2ff5569efabe56839b9e94d0bf72c2f629447ccad39', 'tok': '90f638e6b9f0f8ad40fcc7cf56b49488cb80db00c3655081e259e4a42af8ced5f3bc8251ad5d29a54f1e7',
		    '5': {'key': '3395d6f8f8030784f26f21f149e622cdf2785f29d291b4ac', 'tok': '6b9d81a789b3b05a138f564ecbd540b2be842aaa5dcb7d853459c8105c504083866b339e23974ae51144b'},
		    '6': {'key': '0606c1f425be671cccf8b068bc2d2a3071878603a446758c', 'tok': 'f934536a613016d78ae189e8ed7cfdd7b83605d13aeeb406d6a9e6b8353296344a2b657f584e911d7d0b3'}}}
		j = 0
		while True:
			if l == 1:
			    if j == 6:
			    	j=0
			    j+=1
			    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Api-Key': kkkk[str(j)]['key']}
			    url = 'https://api-public.bosslike.ru/v1/bots/tasks/'
			    res = requests.get(url, params={'service_type': 1, 'task_type': 3}, headers=headers)
			    info = res.json()['data']['items']
			    for i in info:
			        try:
			            ids = i['id']
			            nach = requests.get(f'https://api-public.bosslike.ru/v1/bots/tasks/{ids}/do/', headers=headers)
			            nach = nach.json()['data']['social_metadata']['id']
			            vk_session = vk_api.VkApi(token=kkkk[str(j)]['tok'])
			            vk = vk_session.get_api()
			            try:
			                if str(i['name']['action']) == 'Подписаться на страницу':
			                	vk.groups.join(group_id=nach)
			                else:
			                	vk.friends.add(user_id=nach)
			            except vk_api.Captcha:
			                cycle = True
			                while cycle:
			                    try:
			                        if str(i['name']['action']) == 'Подписаться на страницу':
			                        	vk.groups.join(group_id=nach)
			                        else:
			                        	vk.friends.add(user_id=nach)
			                        yes +=1
			                    except vk_api.Captcha as cptch:
			                        result_solve_captcha = vc.solve(sid=int(cptch.sid), s=1)
			                        try:
			                            cptch.try_again(result_solve_captcha)
			                            cycle = False
			                            yes +=1
			                        except vk_api.Captcha as cptch2:
			                            pass
			                    except:
			                        pass
			            except:
			                pass
			            sleep(1)
			            check = requests.get(f'https://api-public.bosslike.ru/v1/bots/tasks/{int(ids)}/check/', headers=headers)
			        except:
			            requests.get(f'https://api-public.bosslike.ru/v1/bots/tasks/{ids}/hide/', headers=headers)
			else:
				bot.send_message(message.from_user.id, f"Закончена!", reply_markup=markup)
				return


	@bot.message_handler()
	def get_text_messages(message):
	    global l
	    messages = message.from_user.id
	    mess = message.text.lower()
	    if mess == "/start":
	        bot.send_message(messages, f"Работает!", reply_markup=markup)
	    elif mess[0:5] == 'старт':
	    	if l == 0:
	    		l=1
	    		bot.send_message(messages, f"Запущено!", reply_markup=markup)
	    		ferma()
	    	else:
	    		bot.send_message(messages, f"И так запущено!", reply_markup=markup)
	    elif mess == 'стоп':
	    	if l == 1:
	    		l=0
	    		bot.send_message(messages, f"Остановка..", reply_markup=markup)
	    	else:
	    		bot.send_message(messages, f"Останавливать нечего!", reply_markup=markup)
	bot.polling(none_stop=True, interval=0)
except:
	os.system('python bot.py')
