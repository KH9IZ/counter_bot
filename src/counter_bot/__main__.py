import sys
from .runners import (
    long_polling,
    set_webhook,
)

cfg_path = sys.argv[1] if len(sys.argv) > 1 else None
if cfg_path == 'set_webhook':
    set_webhook(sys.argv[2] if len(sys.argv) > 2 else None)
else:
    polling(cfg_path)
