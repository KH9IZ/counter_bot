#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from flask import Flask
from telebot import TeleBot
from telebot.types import ForceReply
from telebot.util import quick_markup


app = Flask(__name__)


with open('token', 'r') as f:
    bot = TeleBot(f.read().strip())


@app.route(f'/bot{bot.token}', methods=['GET', 'POST'])
def bot_route():
    if request.is_json:
        update = Update.de_json(request.json)
        bot.process_new_updates([update])
    else:
        flask.abort(403)


@bot.message_handler(commands=['start', 'create'])
def new_counter(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    sent = bot.send_message(
        chat_id=msg.chat.id, 
        text="Counter\n\nCounts: 0",
        reply_markup=quick_markup({
            "-1": dict(callback_data='-1'),
            "+1": dict(callback_data='+1'),
        }),
    )
    

@bot.message_handler(
    func=lambda msg: msg.reply_to_message and msg.reply_to_message.text.startswith('Counter'),
)
def edit_name(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    name, _, suffix = msg.reply_to_message.text.partition('\n\n')
    bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=msg.reply_to_message.message_id,
        text=f"Counter {msg.text}\n\n{suffix}",
        reply_markup=quick_markup({
            "-1": dict(callback_data='-1'),
            "+1": dict(callback_data='+1'),
        }),
    )


@bot.callback_query_handler(lambda c: c.data in {'-1', '+1'})
def count(c):
    prefix, _, suffix = c.message.text.rpartition(' ')
    cnt = int(suffix)
    button = int(c.data)
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=f"{prefix} {cnt+button}",
        reply_markup=quick_markup({
            "-1": dict(callback_data='-1'),
            "+1": dict(callback_data='+1'),
        }),
    )
    bot.answer_callback_query(c.id)


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 
                                    'text', 'location', 'contact', 'sticker', 'dice'])
def fallback(msg):
    bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


if __name__ == "__main__":
    bot.infinity_polling()
