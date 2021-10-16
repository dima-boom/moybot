try:
	import vk_api, os
	from time import sleep
	vk_session = vk_api.VkApi(token='02f56c62cd91f86c2a2aeb3cbddf58082270251a90b73ca9c08109fe34fd7b9ccf4fe50b5d1a1c7db24cf')
	vk = vk_session.get_api()
	while True:
		sleep(5)
		zav = vk.friends.getRequests(count=20, out=0)
		zav = zav['items']
		k = len(zav)
		if k >0:
			for i in zav:
				try:
					vk.friends.add(user_id=i)
				except:
					pass
except:
	os.system('python bot.py')
