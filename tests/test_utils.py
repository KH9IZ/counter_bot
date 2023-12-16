# -*- coding: utf-8 -*-
import json
from unittest import TestCase
import os
from tempfile import NamedTemporaryFile

from counter_bot.main import (
    bot,
    get_config,
    create_wsgi_app,
)


class GetConfigTestCase(TestCase):
    def test_get_config_no_config(self):
        os.environ.pop('BOT_CONFIG_PATH')
        with self.assertRaises(ValueError) as cm:
            get_config()
        self.assertEqual(
            cm.exception.args[0],
            "Specify BOT_CONFIG_PATH variable",
        )

    def test_get_config_no_file(self):
        bad_path = '/dummy/path'
        with self.assertRaises(ValueError) as cm:
            get_config(bad_path)
        self.assertEqual(
            cm.exception.args[0],
            f"No such path {bad_path}",
        )

    def test_get_config(self):
        test_config = dict(
            TOKEN='dummy_token',
            WEBHOOK_URL='https://dummy.my/url?really=1',
            WEBHOOK_PUB_CERT='/path/to/pub.crt',
        )
        self.cfg_file = NamedTemporaryFile('w+t')
        self.cfg_file.write(json.dumps(test_config))
        self.cfg_file.seek(0)
        cfg = get_config(self.cfg_file.name)
        self.assertEqual(cfg, test_config)
        self.cfg_file.seek(0)
        os.environ['BOT_CONFIG_PATH'] = self.cfg_file.name
        cfg = get_config()
        self.assertEqual(cfg, test_config)


class CreateWSGIAppTestCase(TestCase):
    test_config = {}

    def setUp(self):
        self.test_config = dict(
            TOKEN='not_dummy_token',
            WEBHOOK_URL='https://dummy.my/url?really=1',
            WEBHOOK_PUB_CERT='/path/to/pub.crt',
        )
        self.cfg_file = NamedTemporaryFile('wt')
        self.cfg_file.write(json.dumps(self.test_config))
        self.cfg_file.seek(0)
        os.environ['BOT_CONFIG_PATH'] = self.cfg_file.name

    def test_ok(self):
        app = create_wsgi_app()

        self.assertEqual(
            bot.token,
            self.test_config['TOKEN'],
        )
        self.assertTrue(callable(app))

    def test_no_token(self):
        self.test_config.pop('TOKEN')
        self.cfg_file.truncate(0)
        self.cfg_file.write(json.dumps(self.test_config))
        self.cfg_file.seek(0)
        with self.assertRaises(ValueError) as cm:
            create_wsgi_app()
        self.assertEqual( 
            cm.exception.args[0],
            'Specify TOKEN',
        )
