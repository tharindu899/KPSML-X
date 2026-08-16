if ! command -v mkvpropedit >/dev/null 2>&1; then
    echo "[start.sh] mkvtoolnix not found, installing (needed for split-part duration metadata)..."
    apt-get update -qq && apt-get install -y --no-install-recommends mkvtoolnix -qq > /dev/null 2>&1
fi
python3 update.py && python3 -m bot
