# -*- coding: utf-8 -*-
import json
from unittest import TestCase

from telebot import apihelper
from telebot.types import Dice

from counter_bot import bot
from tests.utils import build_message
from tests.base import (
    BaseBotTestCase,
    TEST_COUNTER_TEMPLATE,
    TEST_REPLY_TO_MESSAGE,
)


class EditCounterTestCase(BaseBotTestCase):
    bot = bot

    def setUp(self):
        super().setUp()
        self.tg_faker.response_value(method='deleteMessage', result=True)
        self.tg_faker.response_value(method='editMessageText', result='{"message_id": 10, "date": 10, "chat": {"id": 1, "type": "private"}}')

    def test_ok(self):
        self.receive_message(
            message_id=2, 
            text='new_name', 
            reply_to=build_message(message_id=1,text=TEST_REPLY_TO_MESSAGE.format(counter_name='', cnt=0)),
        )

        self.process_updates()

        self.assertEqual(len(self.tg_faker.requests), 2)
        self.assertEqual(self.tg_faker.requests[0].params, dict(chat_id=1, message_id=2))
        self.assertEqual(
            self.tg_faker.requests[1].params, 
            dict(
                chat_id=1, 
                message_id=1,
                parse_mode='markdown',
                reply_markup=json.dumps(dict(
                    inline_keyboard=[
                        [
                            dict(text="-1", callback_data='-1'), 
                            dict(text="+1", callback_data='+1'), 
                        ],
                    ],
                )),
                text=TEST_COUNTER_TEMPLATE.format(counter_name="new_name", cnt=0),
            ),
        )

    def test_bad_content_type(self):
        # на самом деле телеграм запрещает удалять дайсы для всех
        # но в тестах можно допустить обратное
        self.receive_message(
            message_id=2, 
            reply_to=build_message(message_id=1,text="Counter\n\nCounts: 0"),
            content_type='dice',
            dice=Dice(value=1, emoji='🎰'),
        )
        self.process_updates()
        self.assertEqual(len(self.tg_faker.requests), 1)
        self.assertEqual(self.tg_faker.requests[0].params, dict(chat_id=1, message_id=2))
