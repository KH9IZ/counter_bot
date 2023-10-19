# -*- coding: utf-8 -*-
import json

from telebot import apihelper
from unittest import TestCase

from counter_bot import bot
from tests.utils import build_message
from tests.base import (
    BaseBotTestCase,
    TEST_COUNTER_TEMPLATE,
)


class CreateCounterTestCase(BaseBotTestCase):
    bot = bot

    def setUp(self):
        super().setUp()
        self.tg_faker.response_value(method='deleteMessage', result=True)
        self.tg_faker.response_value(method='sendMessage', result='{"message_id": 10, "date": 10, "chat": {"id": 1, "type": "private"}}')

    def test_ok(self):
        self.receive_message(message_id=1, text='/start')

        self.process_updates()

        self.assertEqual(len(self.tg_faker.requests), 2)
        self.assertEqual(self.tg_faker.requests[0].params, dict(chat_id=1, message_id=1))
        self.assertEqual(
            self.tg_faker.requests[1].params, 
            dict(
                chat_id='1', 
                parse_mode='markdown',
                reply_markup=json.dumps(dict(
                    inline_keyboard=[
                        [
                            dict(text="-1", callback_data='-1'), 
                            dict(text="+1", callback_data='+1'), 
                        ],
                    ],
                )),
                text=TEST_COUNTER_TEMPLATE.format(counter_name='', cnt=0),
            ),
        )
        
    def test_ok_create(self):
        self.receive_message(message_id=1, text='/create')

        self.process_updates()

        self.assertEqual(len(self.tg_faker.requests), 2)
        self.assertEqual(self.tg_faker.requests[0].params, dict(chat_id=1, message_id=1))
