# ==========================================
# Telegram Userbot /dl com Anti-Flood
# Criador: Nago.rlz
# Linguagem: Python
# Biblioteca: Telethon
# ==========================================

import re
import os
import time
import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.types import MessageEntityBlockquote
from telethon.errors import FloodWaitError

api_id = 1234567890 # TROQUE PELO SEU ID
api_hash = "SUA_API_HASH_AQUU"
string_session = "SUA_STRING_SESSION_AQUI"

# 👉 CANAL FIXO DE ENVIO
TARGET_CHANNEL = -1001234567890  # troca pelo seu id

client = TelegramClient(
    StringSession(string_session),
    api_id,
    api_hash
)

_progress_state = {}

def progress(current, total, prefix=""):
    now = time.monotonic()
    state = _progress_state.get(prefix)

    if not state:
        _progress_state[prefix] = {"time": now, "bytes": current}
        return

    dt = now - state["time"]
    db = current - state["bytes"]
    if dt <= 0:
        return

    speed = db / dt
    speed_mb = speed / (1024 * 1024)
    percent = (current / total) * 100 if total else 0
    eta = (total - current) / speed if speed > 0 else 0

    _progress_state[prefix] = {"time": now, "bytes": current}

    print(
        f"{prefix}{percent:6.2f}% | "
        f"{speed_mb:6.2f} MB/s | ETA {int(eta)}s",
        end="\r"
    )

async def safe_sleep(s):
    await asyncio.sleep(s + 1)

async def is_premium():
    return bool((await client.get_me()).premium)

async def get_max_size():
    return int((3.95 if await is_premium() else 1.95) * 1024**3)

def parse_link(link):
    m = re.search(r"t\.me/(c/)?([^/]+)/(\d+)", link)
    if not m:
        return None
    if m.group(1):
        return int(f"-100{m.group(2)}"), int(m.group(3))
    return m.group(2), int(m.group(3))

def extract_caption(msg):
    if not msg.text:
        return None
    text = msg.text
    entities = msg.entities or []
    out, last = "", 0
    for e in entities:
        if isinstance(e, MessageEntityBlockquote):
            s, e2 = e.offset, e.offset + e.length
            out += text[last:s]
            out += "\n> " + text[s:e2].replace("\n", "\n> ") + "\n"
            last = e2
    out += text[last:]
    return out.strip()

async def safe_send_files(messages, caption):
    while True:
        try:
            await client.send_file(
                TARGET_CHANNEL,
                [m.media for m in messages if m.media],
                caption=caption,
                supports_streaming=True,
                force_document=False,
                progress_callback=lambda c, t: progress(c, t, "⬆️ Upload: ")
            )
            print()
            return

        except Exception:
            print("🔒 Reupload necessário")
            files = []

            for m in messages:
                f = await client.download_media(
                    m.media,
                    progress_callback=lambda c, t: progress(c, t, "⬇️ Download: ")
                )
                print()
                if m.video and f and not f.endswith(".mp4"):
                    nf = f + ".mp4"
                    os.rename(f, nf)
                    f = nf
                files.append(f)

            await client.send_file(
                TARGET_CHANNEL,
                files,
                caption=caption,
                supports_streaming=True,
                force_document=False,
                progress_callback=lambda c, t: progress(c, t, "⬆️ Upload: ")
            )
            print()

            for f in files:
                try: os.remove(f)
                except: pass
            return

@client.on(events.NewMessage(pattern=r'^/dl '))
async def downloader(event):
    _, link, qty = event.raw_text.split()
    qty = int(qty)

    parsed = parse_link(link)
    if not parsed:
        await event.reply("❌ Link inválido.")
        return

    chat, start_id = parsed
    sent = 0
    current = start_id
    used_ids = set()
    max_size = await get_max_size()

    await event.reply(f"📥 Enviando {qty} posts para o canal fixo")

    while sent < qty:
        msg = await client.get_messages(chat, ids=current)
        current -= 1

        if not msg or not msg.media or msg.id in used_ids:
            continue

        if msg.grouped_id:
            album = []
            async for m in client.iter_messages(chat, min_id=msg.id - 10, max_id=msg.id + 10):
                if m.grouped_id == msg.grouped_id:
                    album.append(m)
                    used_ids.add(m.id)
            album.sort(key=lambda x: x.id)
            messages = album
        else:
            used_ids.add(msg.id)
            messages = [msg]

        if any(m.file and m.file.size > max_size for m in messages):
            continue

        caption = None
        for m in messages:
            caption = extract_caption(m)
            if caption:
                break

        await safe_send_files(messages, caption)
        sent += 1
        await asyncio.sleep(1)

    await event.reply("✅ Finalizado sem repetição.")

print("🚀 Userbot ativo | sem posts repetidos | canal fixo")
client.start()
client.run_until_disconnected()
