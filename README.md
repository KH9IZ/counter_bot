# Counter bot
Trivial telegram bot for counting everything.

Project structure: [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

### How to run locally by long polling
Create simple json file with your bot token:
```json
{"TOKEN": "bot123:abc"}
```
Then run with path to your config: `python3 -m counter_bot '/path/to/cfg.json'`

### How to app for WSGI server (on gunicorn as an example)
Create json file:
```json
{
  "TOKEN": "bot:123abc",
  "WEBHOOK_URL": "https://<your_server_domain>/bot<token>",
  "WEBHOOK_PUB_CERT": "/path/to/pub.crt"
}
```

To run bot on your server run `gunicorn counter_bot:create_app('/path/to/config.json')`

!!When bot started, you need to open in your browser https://<your_server_domain>/reset\_webhooks

## Road maps

### Road map bot
[x] MVP
[x] webhooks
[ ] Async

### Road map tests
[x] unittest
[ ] pytest
[ ] tox

### Road map building
[x] setuptools
[ ] poetry

### Road map deplayment
[x] Manual deployment
[ ] GitHub Actions

### Road map servers
[x] Simple server
[ ] Serverless

### Road map infrastructure
[x] Prod
[ ] Testing

### Road map documentation
[x] README
[ ] docs external / internal

### Road map logging
[ ] logging

### Flaker
[ ] pyflake
[ ] black
