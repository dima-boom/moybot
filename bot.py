try:
	import vk_api, psycopg2, os
	from vk_api.utils import get_random_id
	from vk_api.longpoll import VkLongPoll, VkEventType


	con = psycopg2.connect(
	  database="d7gn8mie2vln0r", 
	  user="tjcxpdmxandllx", 
	  password="63d4cc9098f539c586ae3f90d7f24447eb8952d43ca5440ec8d477714448076d", 
	  host="ec2-52-214-125-106.eu-west-1.compute.amazonaws.com", 
	  port="5432"
	)
	cur = con.cursor()
	cur.execute('''CREATE TABLE IF NOT EXISTS baza(
	    vop TEXT,
	    otvet TEXT);''')
	con.commit() 

	cur.execute('''CREATE TABLE IF NOT EXISTS tab(
	    id BIGINT,
	    vop TEXT);''')
	con.commit() 

	def write_message(sender, message):
	    authorize.get_api().messages.send(user_id=sender, message=message, random_id=0)



	token = "8aeca9c1696fced0f6073afb4e26f4b7f89e65c2ea29e0b6018e855e0dd5e98f606ad63e57a5afd345ad1"
	authorize = vk_api.VkApi(token=token)
	longpoll = VkLongPoll(authorize)
	admin = 574170405
	for event in longpoll.listen():
	    if event.type == VkEventType.MESSAGE_NEW and event.text:
	        reseived_message = event.text.lower()
	        sender = event.user_id
	        if event.to_me:
	            # ПРОВЕРКА НА ССЫЛКИ
	            a = 0
	            b = 4
	            opg = 0
	            for i in range(len(reseived_message)):
	                sms = str(reseived_message[a:b])  # 4 Элемента
	                sms2 = str(reseived_message[a:b - 1])  # 3 Элемента
	                sms3 = str(reseived_message[a:b + 1])  # 5 Элементов
	                if sms == "http" or sms == "www." or sms2 == ".ru" or sms == ".com" or sms == ".org" or sms == ".net" or sms2 == ".su" or sms3 == ".shop" or sms2 == ".рф" or sms == ".bar" or sms == ".xyz" or sms2 == ".io":
	                    opg = 1
	                    continue
	            if opg == 1:
	            	continue
	            cur.execute("SELECT * FROM baza")
	            j = cur.fetchall()
	            hjhj = 0
	            for yexy in j:
	                if reseived_message == str(yexy[0]):
	                    write_message(sender, str(yexy[1]))
	                    hjhj = 1
	                    continue
	            if hjhj == 1:
	            	continue
	            cur.execute(f"SELECT vop FROM tab WHERE id = {sender}")
	            ty = cur.fetchall()
	            if str(ty) == '[]':
	                cur.execute(f"""INSERT INTO tab (id, vop) VALUES ({sender}, '{reseived_message}');""")
	                con.commit()
	            else:
	                cur.execute(f"""UPDATE tab SET vop = '{reseived_message}' WHERE id = {sender}""")
	                con.commit() 
	        else:
	            cur.execute(f"SELECT vop FROM tab WHERE id = '{sender}'")
	            df = cur.fetchall()
	            if str(df) != '[]':
	                cur.execute(f"SELECT otvet FROM baza WHERE vop = '{df[0][0]}'")
	                if str(cur.fetchall()) == '[]':
	                    cur.execute(f"""INSERT INTO baza (vop, otvet) VALUES ('{df[0][0]}', '{event.text}');""")
	                    con.commit()
	                else:
	                    pass
except:
	os.system('python bot.py')
