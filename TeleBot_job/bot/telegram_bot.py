import pandas as pd
from numba import typeof
from telegram import Bot
import datetime
import csv
import os
import pyshorteners
from job_finder.TeleBot_job.filters.extract_job_id import is_job_already_sent

class TelegramNotifier:
    def __init__(self, token: str, chat_id: str , log_file="data/sent_jobs.csv"):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.log_file = log_file
        self.s = pyshorteners.Shortener()
        # ודא שה־CSV קיים
        if not os.path.exists(self.log_file):
            with open(self.log_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["message_id", "job_title", "date" , 'link'])
                # קרא את כל הלינקים שכבר נשלחו

        self.links = set()
        try:
            df = pd.read_csv(self.log_file)
            if "link" in df.columns:
                self.links = set(df["link"].dropna())  # סט מאפשר בדיקה מהירה
        except Exception as e:
            print("Error reading CSV:", e)

    async def send_job(self, job: dict, message: str):
        '''


        is_job_exist = is_job_already_sent(sent_links=self.links , new_link=job['link'])
        if is_job_exist:
            text = f"""
-------------------------------------------------------------
                        ⚠️📌 JOB ALREADY EXIST
    ℹ️  Duplicate Job Detected , already been sent before
                🧑‍💼 Title   : {job['title']} , 🏢 company : {job['company']}
-------------------------------------------------------------
"""
            await self.bot.send_message(chat_id=self.chat_id, text=text)
            return
        '''
        now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")

        text = f"""
        💮🌟 NEW JOB FOUND
📆 Date    : {now}
🧑‍💼 Title   : {job['title']}
🏢 company : {job['company']}
🔗 link    : {self.s.tinyurl.short(job['link'])}

📄 Suggested message:
{message}
"""

        sent_message = await self.bot.send_message(chat_id=self.chat_id, text=text)

        # שמירה ב־CSV
        with open(self.log_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([sent_message.message_id, job['title'], now ,job['link']])
