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
import json
import requests
from accounts.models import accountCode, Profile
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
SUPERUSER_USER_ID = os.environ.get('TELEGRAM_USER_ID')
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
	
	# print("url ", url)
	# print("payload ", payload)
	r = requests.post(url, data=payload)
	
	# print(r.status_code)
	# if r.status_code == 200:
	# 	print("Message sent!")
	# else:
	# 	print("some error!")
	# print(r.text)
	return(r.text)
	

# check if chat_id is registered
def check_existing_user(chat_id):
	result = True
	try:
		Profile.objects.get(chat_id=chat_id)
		result = True
	except Profile.DoesNotExist:
		result = False
	finally:
		return(result)

def check_existing_code(chat_id):
	result = True
	try:
		accountCode.objects.get(chat_id=chat_id)
		result = True
	except accountCode.DoesNotExist:
		result = False
	finally:
		return(result)

def get_user_detail(chat_id):
	user = Profile.objects.get(chat_id=chat_id)
	return user
	
# https://getmakerlog.com/apps/telegram?key=3C1393

# create a new accountCode instance. return verify_code
def generate_unique_account_code(chat_id):
	new_instance = accountCode(chat_id=chat_id)
	new_instance.save()
	unique_account_code = new_instance.verify_code
	return unique_account_code

def send_pair_url(chat_id):
	unique_account_code = generate_unique_account_code(chat_id)
	link = 'https://simpleweddingmovement.herokuapp.com/login/?key={}'.format(unique_account_code)
	url  = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
	payload = {"chat_id":chat_id, "text":"📎 Click on 'Pair', and your login credentials", 'reply_markup': json.dumps({"inline_keyboard": [[{"text":"🔑 Pair", "url": link,}]]}) }
	r = requests.post(url, data=payload)
	return(r.text)

def successful_connection(chat_id):
	''' Send message to on telegram '''
	text_message = '''*Successfully connected*'''
	url  = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
	payload = {'text': text_message, 'chat_id':chat_id, 'parse_mode':'Markdown'}
	r = requests.post(url, data=payload)	
	return(r.text)

def please_pair(chat_id):
	''' Send message to on telegram '''
	text_message = '''*Please /pair to use this feature*'''
	url  = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
	payload = {'text': text_message, 'chat_id':chat_id, 'parse_mode':'Markdown'}
	r = requests.post(url, data=payload)
	return(r.text)

def already_connnected(chat_id):
	''' Send message to on telegram '''
	text_message = '''*Please /pair to use this feature*'''
	url  = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
	payload = {'text': text_message, 'chat_id':chat_id, 'parse_mode':'Markdown'}
	r = requests.post(url, data=payload)
	return(r.text)

def profile(chat_id):
	user = get_user_detail(chat_id)
	username = user.user
	full_name = user.user.get_full_name()
	user_bio = user.bio if user.bio is not None else None
	phone_number = user.phone_number if user.phone_number is not None else None
	user_articles = 0
	user_articles_ideas = 0
	user_links = 0

	payload_message = '''
👤 ABOUT
Username : {}
Name : {}
phone number : {}
Bio : {}

✏️ ACTIVITIES
Articles : {}
Article Ideas : {}
Links : {}
	'''.format(username , full_name , phone_number, user_bio, user_articles, user_articles_ideas, user_links)
	link = 'https://simpleweddingmovement.herokuapp.com/login/'
	url  = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
	payload = {"chat_id":chat_id, "text":payload_message, 'reply_markup': json.dumps({"inline_keyboard": [[{"text":"✍️ Edit", "url": link,}]]}) }
	r = requests.post(url, data=payload)
	return(r.text)

def send_help(chat_id):
	text_message = '''
I'm SimpleWeddingBot, your friendly telegram help.
I'll help you manage your account on Simple Wedding Movement website

My task is to encourage you to be more active on the website
You're not logged in.


To begin login, you need to /pair

After logging in, you can
👉 View your account status. (Visitor, Writer, Admin)
👉 View and edit your Name, Phone number and Bio
👉 Disconnect your SWM account from Telegram

To begin login, you need to /pair
	'''.format(user.user.get_full_name)
	url  = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
	payload = {'text': text_message, 'chat_id':chat_id, 'parse_mode':'Markdown'}
	r = requests.post(url, data=payload)
	return(r.text)

def send_help_user(chat_id):
	user = get_user_detail(chat_id)
	text_message = '''
I'm SimpleWeddingBot, your friendly telegram help.

You're logged in as {} on Simple Wedding Movement Site.

I'll help you manage your account on Simple Wedding Movement website

My task is to encourage you to be more active on the website


Your Account:

/mystatus 
View your account status. (Visitor, Writer, Admin)
/profile
View your account details like Name, Phone number and Bio
/editprofile
Edit your account details like Name, Phone number and Bio


Authentication:  

/pair
Connect to my SWM website
/unpair
Disconnect your SWM account from Telegram


Other:  

/help
Read this again
	'''.format(user.user)
	url  = 'https://api.telegram.org/bot{}/sendMessage'.format(TELEGRAM_TOKEN)
	payload = {'text': text_message, 'chat_id':chat_id, 'parse_mode':'Markdown'}
	r = requests.post(url, data=payload)
	return(r.text)


if __name__ == '__main__':
	send_message("Testing from SimpleWeddingBot", "Please connect to this bot to recieve website updates", "Please reply to continue")
