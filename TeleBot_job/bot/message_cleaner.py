from telegram import Bot
import csv
from datetime import datetime

class TelegramCleaner:
    def __init__(self, token: str, chat_id: str, log_file="data/sent_jobs.csv"):
        self.bot = Bot(token=token)
        self.chat_id = chat_id
        self.log_file = log_file

    def delete_old_messages(self):
        today = datetime.now().date()
        rows_to_keep = []

        # קרא את כל ההודעות
        with open(self.log_file, "r", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                msg_date = datetime.strptime(row["date"], "%d/%m/%Y %H:%M:%S").date()
                if msg_date != today:
                    # מחק הודעה ישנה
                    self.bot.delete_message(chat_id=self.chat_id, message_id=int(row["message_id"]))
                else:
                    rows_to_keep.append(row)

        # שמור מחדש את ההודעות של היום בלבד
        with open(self.log_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["message_id", "job_title", "date" , "link"])
            writer.writeheader()
            writer.writerows(rows_to_keep)
