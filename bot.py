from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
updater = Updater(token='775269576:AAE8wfw7t-SUVEcuhlIClHsdT3o5oA976zQ') # Токен API к Telegram
dispatcher = updater.dispatcher


# команды
def startCommand(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text='''Привет!
		Что бы узнать что я умею - нажми /help''')

def helpCommand(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text='''Я могу просто пообщатся с тобой, для этого просто пиши мне!
		Также, я могу поразвлекать тебя, для этого нажми /game !''')

def gameCommand(bot, update):
	bot.send_message(chat_id=update.message.chat_id, text='''
		Нажми /wish что-бы поиграть в игру \"желание\" с друзьями или без!
		Нажми /anekdot что-бы получить случайный анекдот!
		Нажми /fact что-бы получить случайный факт!''')

def anekdotCommand(bot, update):
	request = apiai.ApiAI('5f65bada4d194edf83f22ac9e5f1cf19').text_request() # Токен API к Dialogflow
	request.lang = 'ru' # На каком языке будет послан запрос
	request.session_id = 'Intelligent_Assistant_Bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
	request.query = "Расскажи анекдот" # Статический запрос для получения анекдота
	responseJson = json.loads(request.getresponse().read().decode('utf-8'))
	response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
	if response:
		bot.send_message(chat_id=update.message.chat_id, text='''{}
			Посмеялся? Нажми /anekdot что бы получить еще один анекдот'''.format(response))

def factCommand(bot, update):
	request = apiai.ApiAI('5f65bada4d194edf83f22ac9e5f1cf19').text_request() # Токен API к Dialogflow
	request.lang = 'ru' # На каком языке будет послан запрос
	request.session_id = 'Intelligent_Assistant_Bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
	request.query = "Расскажи факт" # Статический запрос для получения анекдота
	responseJson = json.loads(request.getresponse().read().decode('utf-8'))
	response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
	if response:
		bot.send_message(chat_id=update.message.chat_id, text='''{}
			Интересно? Нажми /fact что бы получить еще один факт'''.format(response))

def wishCommand(bot, update):
	flag = True
	bot.send_message(chat_id=update.message.chat_id, text='''Я буду загадывать тебе задания, а ты их выполняй!
		Если захочешь прекратить игру - нажми /cancel 
		Что бы получить желание - нажимай /nextwish''')

def nextWishCommand(bot, update):
	request = apiai.ApiAI('5f65bada4d194edf83f22ac9e5f1cf19').text_request() # Токен API к Dialogflow
	request.lang = 'ru' # На каком языке будет послан запрос
	request.session_id = 'Intelligent_Assistant_Bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
	request.query = "Играем в игру играя" # Статический запрос для получения желания
	responseJson = json.loads(request.getresponse().read().decode('utf-8'))
	response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
	if response:
		bot.send_message(chat_id=update.message.chat_id, text='''{}
			Выполнил? Нажми /nextwish что бы получить следующее желание!
					  Нажми /cancel что бы закончить игру!'''.format(response))

def cancel(bot, update):
	flag = False
	bot.send_message(chat_id=update.message.chat_id, text='''Жалко, было интересно играть!
		Если захочешь еще поиграть - нажми /wish''')
def textMessage(bot, update):
	request = apiai.ApiAI('5f65bada4d194edf83f22ac9e5f1cf19').text_request() # Токен API к Dialogflow
	request.lang = 'ru' # На каком языке будет послан запрос
	request.session_id = 'Intelligent_Assistant_Bot' # ID Сессии диалога (нужно, чтобы потом учить бота)
	request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
	responseJson = json.loads(request.getresponse().read().decode('utf-8'))
	response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
	if response:
		bot.send_message(chat_id=update.message.chat_id, text=response)
	else:
		bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
	
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
help_command_handler = CommandHandler('help', helpCommand)
game_command_handler = CommandHandler('game', gameCommand)
wish_command_handler = CommandHandler('wish', wishCommand)
anekdot_command_handler = CommandHandler('anekdot', anekdotCommand)
fact_command_handler = CommandHandler('fact', factCommand)
cancel_command_handler = CommandHandler('cancel', cancel)
text_message_handler = MessageHandler(Filters.text, textMessage)
next_wish_command_handler = CommandHandler('nextwish', nextWishCommand)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(help_command_handler)
dispatcher.add_handler(game_command_handler)
dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(wish_command_handler)
dispatcher.add_handler(anekdot_command_handler)
dispatcher.add_handler(fact_command_handler)
dispatcher.add_handler(cancel_command_handler)
dispatcher.add_handler(next_wish_command_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
