import telebot
from telebot import formatting
from dotenv import load_dotenv
load_dotenv()
from os import getenv
from messages import *

bot = telebot.TeleBot(getenv("TOKEN")) # type: ignore
counters = dict()

def init_chat(key) -> None:
	"""Initializes chat in counters storage."""
	if key in counters:
		return
	counters[key] = 0

def binary_string(key) -> str:
	"""Gets binary representation of counter for a given chatid."""
	number = counters[key] if key in counters else 0
	return f"{number:b}"

def set(key, num) -> None:
	counters[key] = num

def add(key) -> None:
	counters[key] += 1

@bot.message_handler(commands=["start","help"])
def welcome_message(msg: telebot.types.Message) -> None:
	"""Initializes chat and sends the welcome/help message.
	
	This method is triggered by "/start" and "/help" messages.
	"""
	init_chat(msg.chat.id)
	bot.send_message(msg.chat.id, help_message)

@bot.message_handler(commands=["set"])
def set_value_base10(msg: telebot.types.Message) -> None:
	"""Sets value of the chat assuming base10.
	
	This method is triggered by "/set <num>" message.
	"""
	set_value(msg)

@bot.message_handler(commands=["set_bin"])
def set_value_base2(msg: telebot.types.Message) -> None:
	"""Sets value of the chat assuming base2.
	
	This method is triggered by "/set_bin <num>" message.
	"""
	set_value(msg, 2)

def set_value(msg: telebot.types.Message, base:int = 10) -> None:
	"""Sets value of the chat assuming base2.
	
	This method is indirectly triggered by 
	"/set <num>" and "/set_bin <num>" messages.
	
	If <num> is not a number, bot replies with the nan_error message.
	"""
	num = telebot.util.extract_arguments(msg.text).strip() # type: ignore
	if not num.isdigit():
		bot.reply_to(msg, nan_error)
		return
	set(msg.chat.id, int(num, base))

@bot.message_handler(commands=["get","next"])
def get_value(msg: telebot.types.Message):
	"""Sends the next value to chat.

	This method is triggered by "/get" and "/next" messages.
	"""
	response = formatting.mcode(binary_string(msg.chat.id))
	add(msg.chat.id)
	bot.send_message(msg.chat.id, response, parse_mode="MarkdownV2")

bot.infinity_polling()
