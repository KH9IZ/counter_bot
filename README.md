# Counter bot
Trivial telegram bot for counting everything.

Project structure: [src layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

To run bot on your server run `gunicorn counter_bot:create_app('/etc/counter_bot/config.json')`

config.json:
```json
{
  "TOKEN": "bot:123abc",
  "WEBHOOK_URL": "https://example.com/url",
  "WEBHOOK_PUB_CERT": "/path/to/pub.crt"
}
```

## Road maps

### Road map bot
[x] MVP
[ ] webhooks
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
[ ] README
[ ] docs external / internal

### Road map logging
[ ] logging

### Flaker
[ ] pyflake
[ ] black
