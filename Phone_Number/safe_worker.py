from db_helper import init_db, is_checked, save_checked
import os
import json
import random
import asyncio
import logging
from dotenv import load_dotenv
from telethon import TelegramClient, errors, functions, types
import socks

load_dotenv()
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
FORWARD_CHAT_ID = int(os.getenv("FORWARD_CHAT_ID"))

SESSION_DIR = "session"
QUEUE_FILE = "queue.txt"
PROXY_MAP_FILE = "proxy_map.json"
DELAY = 12

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


with open(PROXY_MAP_FILE, "r") as f:
    PROXY_MAP = json.load(f)

def get_proxy_for_session(session_file):
    proxy_cfg = PROXY_MAP.get(session_file)
    if not proxy_cfg:
        logger.warning(f"⚠️ Không tìm thấy proxy cho {session_file}")
        return None

    proxy_type = socks.SOCKS5 if proxy_cfg["type"] == "socks5" else socks.SOCKS4
    return (
        proxy_type,
        proxy_cfg["host"],
        int(proxy_cfg["port"]),
        True,
        proxy_cfg.get("user"),
        proxy_cfg.get("pass")
    )

def load_queue():
    return open(QUEUE_FILE, "r").read().splitlines() if os.path.exists(QUEUE_FILE) else []

def save_queue(numbers):
    with open(QUEUE_FILE, "w") as f:
        for n in numbers:
            f.write(n + "\n")


async def check_number(phone_number, frozen_sessions):
    session_files = [f for f in os.listdir(SESSION_DIR) if f.endswith(".session") and f not in frozen_sessions]
    if not session_files:
        logger.warning("❌ Hết session hoạt động.")
        return

    random.shuffle(session_files)

    for session_file in session_files:
        session_path = os.path.join(SESSION_DIR, session_file)
        proxy = get_proxy_for_session(session_file)

        client = TelegramClient(session_path, API_ID, API_HASH, proxy=proxy)
        await client.connect()

        try:
            if not await client.is_user_authorized():
                logger.warning(f"⚠️ {session_file} chưa đăng nhập.")
                await client.disconnect()
                continue

            logger.info(f"🔍 Kiểm tra {phone_number} bằng {session_file}")
            contact = types.InputPhoneContact(
                client_id=random.randint(1, 999999),
                phone=phone_number,
                first_name="Check",
                last_name=""
            )

            try:
                result = await client(functions.contacts.ImportContactsRequest([contact]))
            except errors.FloodWaitError as e:
                logger.warning(f"⏳ FloodWait {e.seconds}s → chờ thêm.")
                await asyncio.sleep(e.seconds + 5)
                continue
            except errors.RPCError as e:
                if 'FROZEN_METHOD_INVALID' in str(e):
                    logger.warning(f"🧊 Frozen session: {session_file}")
                    frozen_sessions.add(session_file)
                    break
                else:
                    logger.warning(f"⚠️ RPC lỗi khác: {e}")
                    break

            user = result.users[0] if result.users else None
            if user:
                contact_card = types.InputMediaContact(
                    phone_number=phone_number,
                    first_name=user.first_name or "",
                    last_name=user.last_name or "",
                    vcard=f"BEGIN:VCARD\nVERSION:3.0\nFN:{user.first_name or ''} {user.last_name or ''}\nTEL:{phone_number}\nEND:VCARD"
                )
                await client(functions.messages.SendMediaRequest(
                    peer=FORWARD_CHAT_ID,
                    media=contact_card,
                    message="",
                    random_id=random.randint(100000, 999999999)
                ))
                logger.info(f"✅ {phone_number} có Telegram. Đã gửi contact.")
            else:
                logger.info(f"❌ {phone_number} không dùng Telegram.")

            if user:
                await client(functions.contacts.DeleteContactsRequest(
                    id=[types.InputUser(user.id, user.access_hash)]
                ))

            await asyncio.sleep(DELAY)
            break

        except Exception as e:
            logger.error(f"❌ Lỗi không mong muốn: {e}")
        finally:
            await client.disconnect()


async def main():
    init_db()
    frozen_sessions = set()

    while True:
        queue = load_queue()
        if not queue:
            await asyncio.sleep(5)
            continue

        phone = queue.pop(0)

        if is_checked(phone):
            logger.info(f"⏭️ Đã kiểm: {phone}")
            save_queue(queue)
            continue

        await check_number(phone, frozen_sessions)
        save_checked(phone, status="done")
        save_queue(queue)

if __name__ == "__main__":
    asyncio.run(main())
