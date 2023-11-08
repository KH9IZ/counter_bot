# -*- coding: utf-8 -*-
"""
Different bot runners

Currently supported Yandex Cloud Function and long polling
"""

import json
import logging
import os

from telebot.types import Update

from .main import bot


token = os.getenv('TOKEN')
secret_token = os.getenv('SECRET_TOKEN').strip()
bot.token = token

log = logging.getLogger('counter_bot.runners')
log.setLevel(logging.DEBUG)


def long_polling():
    bot.remove_webhook()
    bot.infinity_polling()


def cloud_function(event, context):
    content_type = event['headers'].get('Content-Type', '')
    secret_token_header = event['headers'].get('X-Telegram-Bot-Api-Secret-Token')
    if not (
        content_type.startswith('application') and 
        content_type.endswith('json') and 
        (secret_token and secret_token == secret_token_header)
    ):
        return {'statusCode': 403, 'body': ''}
    try:
        update = Update.de_json(json.loads(event['body']))
    except (ValueError, KeyError, json.decoder.JSONDecodeError):
        return {'statusCode': 403, 'body': ''}

    bot.process_new_updates([update])
    return {'statusCode': 200, 'body': ''}


def set_webhook(url=None):
    url = url or input("Enter webhook URL: ")
    bot.set_webhook(
        url=url,
        allowed_updates=json.dumps(['message', 'callback_query']),
        secret_token=secret_token,
    )

# TODO: wsgi support + extra docker image
