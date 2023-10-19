from unittest import TestCase

from telebot.types import (
    Update,
    Message,
)
from telebot import apihelper

from tests.tg_faker import TgFaker
from tests.utils import (
    build_callback_query,
    build_message,
    build_update,
)


TEST_COUNTER_TEMPLATE = "🔢 {counter_name}\n\n**{cnt}**"
TEST_REPLY_TO_MESSAGE = "🔢 {counter_name}\n\n{cnt}"


class BaseBotTestCase(TestCase):
    __updates: list[Update]
    __id_counter: int
    bot = None
    
    def setUp(self):
        super().setUp()
        self.__updates = []
        self.__id_counter = 0
        self.tg_faker = TgFaker()
        self.bot.threaded = False
        apihelper.CUSTOM_REQUEST_SENDER = self.tg_faker.request_sender

    def generate_id(self):
        self.__id_counter += 1
        return self.__id_counter

    def receive_message(
        self, 
        message_id=None, 
        content_type=None, 
        text=None, 
        reply_to=None, 
        dice=None,
    ):
        self.receive_update(message=build_message(
            message_id=message_id or self.generate_id(),
            text=text,
            reply_to=reply_to,
            content_type=content_type,
            dice=dice,
        ))

    def receive_callback_query(self, callback_id=None, data=None, message=None):
        self.receive_update(callback_query=build_callback_query(
            callback_id=callback_id or self.generate_id(),
            data=data,
            message=message,
        ))

    def receive_update(self, message=None, callback_query=None):
        if not any((message, callback_query)):
            raise ValueError("Unsupported update type")

        self.__updates.append(build_update(
            update_id=self.generate_id(),
            message=message,
            callback_query=callback_query,
        ))

    def process_updates(self, extra_updates: list[Update] = None):
        if extra_updates:
            self.__updates.extend(extra_updates)

        if self.bot is None:
            raise AttributeError("bot attribute needed")

        self.bot.process_new_updates(self.__updates)
        self.__updates = []
