#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re
from time import sleep

from flask import (
    abort,
    Flask,
    request,
)
from telebot import TeleBot
from telebot.types import (
    ForceReply,
    Update,
)
from telebot.util import quick_markup


PREFIX = "🔢"
COUNTER_TEMPLATE = PREFIX + " {counter_name}\n\n**{cnt}**"
KEYBOARD = quick_markup({
    "-1": dict(callback_data='-1'),
    "+1": dict(callback_data='+1'),
})
RE_TEMPLATE = re.compile(fr"{PREFIX} (?P<counter_name>.*?)\n\n(?P<cnt>-?[0-9][0-9]*)")


def parse_text(text):
    t = RE_TEMPLATE.match(text)
    if t:
        return t.groups()
    return '', 0


app = Flask(__name__)
bot = TeleBot('dummy_token', parse_mode='markdown')


@app.route('/bot<token>', methods=['GET', 'POST'])
def bot_route(token):
    if token != bot.token:
        abort(404)
    if not request.is_json:
        abort(403)

    try:
        update = Update.de_json(request.json)
    except (ValueError, KeyError, json.decoder.JSONDecodeError):
        abort(403)

    bot.process_new_updates([update])
    return ''


@app.route('/reset_webhook', methods=['GET', 'POST'])
def reset_webhook():
    cfg = get_config()
    bot.remove_webhook()
    sleep(0.1)
    with open(cfg['WEBHOOK_PUB_CERT']) as f:
        bot.set_webhook(
            url=cfg.get('WEBHOOK_URL'),
            certificate=f,
        )
    return ''


@bot.message_handler(commands=['start', 'create'])
def new_counter(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    sent = bot.send_message(
        chat_id=msg.chat.id, 
        text=COUNTER_TEMPLATE.format(counter_name='', cnt=0),
        reply_markup=KEYBOARD,
    )
    

@bot.message_handler(
    func=lambda msg: msg.reply_to_message and msg.reply_to_message.text.startswith(PREFIX),
)
def edit_name(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    name, cnt = parse_text(msg.reply_to_message.text)
    bot.edit_message_text(
        chat_id=msg.chat.id,
        message_id=msg.reply_to_message.message_id,
        text=COUNTER_TEMPLATE.format(counter_name=msg.text, cnt=cnt),
        reply_markup=KEYBOARD,
    )


@bot.callback_query_handler(lambda c: c.data in {'-1', '+1'})
def count(c):
    name, cnt = parse_text(c.message.text)
    cnt = int(cnt)
    button = int(c.data)
    bot.edit_message_text(
        chat_id=c.message.chat.id,
        message_id=c.message.message_id,
        text=COUNTER_TEMPLATE.format(counter_name=name, cnt=cnt+button),
        reply_markup=KEYBOARD,
    )
    bot.answer_callback_query(c.id)


@bot.message_handler(content_types=['audio', 'photo', 'voice', 'video', 'document', 
                                    'text', 'location', 'contact', 'sticker', 'dice'])
def fallback(msg):
    bot.delete_message(chat_id=msg.chat.id, message_id=msg.message_id)


def get_config(config_path=None):
    config_path = config_path or os.getenv('BOT_CONFIG_PATH', None)
    if config_path is None:
        raise ValueError(f"Specify BOT_CONFIG_PATH variable")
    if not os.path.exists(config_path):
        raise ValueError(f"No such path {config_path}")

    with open(config_path) as f:
        cfg = json.load(f)

    return cfg


def create_wsgi_app(config_path=None):
    cfg = get_config(config_path)
    if 'TOKEN' not in cfg:
        raise ValueError("Specify TOKEN")
    bot.token = cfg['TOKEN']
    return app


def polling(cfg_path):
    cfg = get_config(cfg_path)
    if 'TOKEN' not in cfg:
        raise ValueError("Specify TOKEN")
    bot.token = cfg['TOKEN']
    bot.remove_webhook()
    bot.infinity_polling()


def cloud_function(event, context):
    # content_type = event['headers']['Content-Type']
    # if not (
    #     content_type.startswith('application') and 
    #     content_type.endswith('json')
    # ):
    #     abort(403)

    bot.token = os.environ['TOKEN']
    try:
        update = Update.de_json(json.loads(event['body']))
    except (ValueError, KeyError, json.decoder.JSONDecodeError):
        return {
            'statusCode': 403,
            'body': '',
        }

    bot.process_new_updates([update])
    return {
        'statusCode': 200,
        'body': '',
    }


if __name__ == "__main__":
    polling(sys.argv[2] if len(sys.argv) >= 2 else None)
