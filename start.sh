python3 - <<'PYEOF'
import sqlite3
import os

session_file = "bot.session"
if os.path.exists(session_file):
    try:
        conn = sqlite3.connect(session_file)
        conn.execute("SELECT number FROM version").fetchone()
        conn.close()
    except sqlite3.Error:
        # Session file exists but has an incompatible/corrupt schema
        # (commonly happens after switching Pyrogram forks). Remove it
        # so a fresh, valid session gets created automatically.
        conn.close()
        os.remove(session_file)
        for extra in ("bot.session-journal", "bot.session-shm", "bot.session-wal"):
            if os.path.exists(extra):
                os.remove(extra)
        print(f"[start.sh] Removed incompatible {session_file}; a fresh one will be created.")
PYEOF

python3 update.py && python3 -m bot
