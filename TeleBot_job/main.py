import asyncio
import json
import warnings

from bot.telegram_bot import TelegramNotifier
from bot.message_cleaner import TelegramCleaner
from filters.job_filter import is_relevant
from generator.message_builder import build_message
from scraper.linkedin_jobs import fetch_jobs

warnings.filterwarnings("ignore", category=RuntimeWarning)

with open("/Users/shryqb/PycharmProjects/job_finder/TeleBot_job/detail.json", "r") as f:
    json_data = json.load(f)
TELEGRAM_TOKEN = json_data['TOKEN']
CHAT_ID = json_data['CHAT_ID']



async def main():
    # 1️⃣ מחיקת הודעות ישנות לפני שליחה
    TelegramCleaner(TELEGRAM_TOKEN, CHAT_ID).delete_old_messages()


    # 2️⃣ יצירת הבוט
    notifier = TelegramNotifier(TELEGRAM_TOKEN, CHAT_ID)

    # 3️⃣ הבאת משרות
    jobs = fetch_jobs(keywords="data", location="Israel")

    # 4️⃣ סינון ושליחה
    for job in jobs:
        if is_relevant(job):
            message = build_message(job)
            await notifier.send_job(job, message)

# --- הרצת הבוט ---


if __name__ == "__main__":

    asyncio.run(main())

