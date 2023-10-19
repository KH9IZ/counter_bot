# -*- coding: utf-8 -*-
import json
from unittest import TestCase

from telebot import apihelper
from telebot.types import Dice

from counter_bot.main import app, bot
from tests.utils import build_message
from tests.base import BaseBotTestCase


TEST_ROUTE = '/botdummy_token'


class RouteTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.bot = bot
        self.app = app.test_client()

    def test_ok(self):
        rv = self.app.post(TEST_ROUTE, content_type='application/json', data='{"update_id": 1}')
        self.assertEqual(rv.status_code, 200)

    def test_misroute(self):
        routes = ['/ugly', '/bot', '/bot123']
        for route in routes:
            rv = self.app.post(route, content_type='application/json', data='{"update_id": 1}')
            self.assertEqual(rv.status_code, 404)

    def test_invalid_data(self):
        datas = [
            {},
            dict(update_id=1, message=1),
            dict(update_id=1, message=""),
            dict(update_id=1, message={}),
        ]
        for data in datas:
            rv = self.app.post(TEST_ROUTE, content_type='application/json', data=json.dumps(data))
            self.assertEqual(rv.status_code, 403, data)

    def test_invalid_mime_type(self):
        rv = self.app.post(TEST_ROUTE, content_type='application/xml', data='{"update_id": 1}')
        self.assertEqual(rv.status_code, 403)
