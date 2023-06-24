import telebot
from dotenv import load_dotenv
load_dotenv()
from os import getenv
from messages import *

bot = telebot.TeleBot(getenv("TOKEN"))
counters = dict()

def init_user(key):
	if key in counters:
		return
	counters[key] = 0

def binary_string(key):
	number = counters[key] if key in counters else 0
	return f"{number:b}"

def set(key, num):
	counters[key] = num

def add(key):
	counters[key] += 1

@bot.message_handler(commands=["start","help"])
def welcome_message(msg):
	init_user(msg.chat.id)
	bot.send_message(msg.chat.id, help_message)

@bot.message_handler(commands=["set"])
def set_value(msg):
	num = telebot.util.extract_arguments(msg.text).strip()
	if not num.isdigit():
		bot.reply_to(msg, nan_error)
	set(msg.chat.id, int(num))

@bot.message_handler(commands=["next"])
def get_value(msg):
	response = telebot.formatting.mcode(binary_string(msg.chat.id))
	add(msg.chat.id)
	bot.send_message(msg.chat.id, response, parse_mode="MarkdownV2")

bot.infinity_polling()
