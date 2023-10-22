import sys
from .main import polling

cfg_path = sys.argv[1] if len(sys.argv) > 1 else None
polling(cfg_path)
