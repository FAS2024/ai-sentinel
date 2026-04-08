import os
import sys
import tempfile
from pathlib import Path

# Tests must set DATABASE_URL before any backend import (engine binds at import time).
_fd, _TEST_DB_PATH = tempfile.mkstemp(suffix="_ai_sentinel_test.db")
os.close(_fd)
Path(_TEST_DB_PATH).unlink(missing_ok=True)
os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{Path(_TEST_DB_PATH).resolve().as_posix()}"
os.environ.setdefault("REDIS_URL", "redis://127.0.0.1:6379/0")

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
