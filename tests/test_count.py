# -*- coding: utf-8 -*-
import json
from unittest import TestCase

from telebot import apihelper
from telebot.types import Dice

from main import bot
from tests.utils import build_message
from tests.base import BaseBotTestCase


class CountTestCase(BaseBotTestCase):
    bot = bot

    def setUp(self):
        super().setUp()
        self.tg_faker.response_value(method='editMessageText', result='{"message_id": 10, "date": 10, "chat": {"id": 1, "type": "private"}}')
        self.tg_faker.response_value(method='answerCallbackQuery', result=True)

    def test_ok_plus(self):
        self.receive_callback_query(callback_id=1, data='+1', message=build_message(message_id=1, text="Counter\n\nCounts: 0"))

        self.process_updates()

        self.assertEqual(len(self.tg_faker.requests), 2)
        self.assertEqual(
            self.tg_faker.requests[0].params, 
            dict(
                chat_id=1, 
                message_id=1,
                reply_markup=json.dumps(dict(
                    inline_keyboard=[
                        [
                            dict(text="-1", callback_data='-1'), 
                            dict(text="+1", callback_data='+1'), 
                        ],
                    ],
                )),
                text="Counter\n\nCounts: 1",
            ),
        )
        self.assertEqual(self.tg_faker.requests[1].params, dict(callback_query_id=1))

    def test_ok_minus(self):
        self.receive_callback_query(callback_id=1, data='-1', message=build_message(message_id=1, text="Counter\n\nCounts: 0"))

        self.process_updates()

        self.assertEqual(len(self.tg_faker.requests), 2)
        self.assertEqual(
            self.tg_faker.requests[0].params, 
            dict(
                chat_id=1, 
                message_id=1,
                reply_markup=json.dumps(dict(
                    inline_keyboard=[
                        [
                            dict(text="-1", callback_data='-1'), 
                            dict(text="+1", callback_data='+1'), 
                        ],
                    ],
                )),
                text="Counter\n\nCounts: -1",
            ),
        )
        self.assertEqual(self.tg_faker.requests[1].params, dict(callback_query_id=1))
