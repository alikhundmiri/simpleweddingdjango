'''
Done! Congratulations on your new bot. 

You will find it at t.me/SimpleWeddingBot. 

You can now add a description, about section and profile picture for your bot, see /help for a list of commands. 
By the way, when you've finished creating your cool bot, ping our Bot Support if you want a better username for it. 
Just make sure the bot is fully operational before you do this.

Use this token to access the HTTP API: TELEGRAM_TOKEN

Keep your token secure and store it safely, it can be used by anyone to control your bot.

For a description of the Bot API, see this page: https://core.telegram.org/bots/api
'''

import os
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
print(TELEGRAM_TOKEN)

TELEGRAM_USER_ID = os.environ.get('TELEGRAM_USER_ID')
'''
https://api.telegram.org/botfiajsdv;oijl/setWebhook?url=https://simpleweddingmovement.herokuapp.com/tbot
https://api.telegram.org/botdslijv;dlijv/getWebhookInfo
'''

def send_message(title, text, subtitle, chat_id):
	''' Send message to on telegram '''
	text_message = '''*{}*
{}
_{}_'''.format(title, text, subtitle)
	url  = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
	payload = {'text': text_message, 'chat_id':chat_id, 'parse_mode':'Markdown'}
	
	print("url ", url)
	print("payload ", payload)
	r = requests.post(url, data=payload)
	
	print(r.status_code)
	if r.status_code == 200:
		print("Message sent!")
	else:
		print("some error!")
	print(r.text)
	return(r.text)
	
if __name__ == '__main__':
	send_message("Testing from SimpleWeddingBot", "Please connect to this bot to recieve website updates", "Please reply to continue")
