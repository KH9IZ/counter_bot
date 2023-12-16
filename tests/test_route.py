# -*- coding: utf-8 -*-
import json
from unittest import TestCase
import os
from tempfile import NamedTemporaryFile

from telebot import apihelper

from counter_bot.main import app, bot
from tests.tg_faker import TgFaker


class BaseRouteTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.bot = bot
        self.app = app.test_client()
        self.tg_faker = TgFaker()
        self.bot.threaded = False
        apihelper.CUSTOM_REQUEST_SENDER = self.tg_faker.request_sender


class BotRouteTestCase(BaseRouteTestCase):
    url = '/botdummy_token'

    def test_ok(self):
        rv = self.app.post(self.url, content_type='application/json', data='{"update_id": 1}')
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
            rv = self.app.post(self.url, content_type='application/json', data=json.dumps(data))
            self.assertEqual(rv.status_code, 403, data)

    def test_invalid_mime_type(self):
        rv = self.app.post(self.url, content_type='application/xml', data='{"update_id": 1}')
        self.assertEqual(rv.status_code, 403)


class ResetWebhookTestCase(BaseRouteTestCase):
    url = '/reset_webhook'

    def setUp(self):
        super().setUp()
        self.tg_faker.response_value(method='setWebhook', result=True)

        self.cert_file = NamedTemporaryFile('w+t')
        self.cert_file.write('some_public_certificate')
        self.cert_file.seek(0)
        self.cfg_file = NamedTemporaryFile('w+t')
        self.cfg_file.write(json.dumps(dict(
            TOKEN='dummy_token',
            WEBHOOK_URL='https://dummy.my/url?really=1',
            WEBHOOK_PUB_CERT=self.cert_file.name,
        )))
        self.cfg_file.seek(0)
        os.environ['BOT_CONFIG_PATH'] = self.cfg_file.name

    
    def test_ok(self):
        rv = self.app.get(self.url, content_type='application/json')
        self.assertEqual(rv.status_code, 200)
        self.assertEqual(len(self.tg_faker.requests), 2)
        self.assertEqual(
            self.tg_faker.requests[0].params, 
            {'url': ''},
        )
        self.assertEqual(
            self.tg_faker.requests[1].params, 
            {'url': 'https://dummy.my/url?really=1'},
        )
        self.assertEqual(
            self.tg_faker.requests[1].files['certificate'].name,
            self.cert_file.name,
        )

