from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from telegram import Update
from bot.telegram_bot import TelegramNotifier
from scraper.linkedin_jobs import fetch_jobs
from filters.job_filter import is_relevant
from generator.message_builder import build_message
import json

import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)

with open("/Users/shryqb/PycharmProjects/job_finder/TeleBot_job/detail.json", "r") as f:
    json_data = json.load(f)
TOKEN = json_data['TOKEN']
CHAT_ID = json_data['CHAT_ID']

notifier = TelegramNotifier(TOKEN, CHAT_ID)

# פקודת /jobs
async def jobs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    jobs = fetch_jobs(keywords="data", location="Israel")
    sent_count = 0
    for job in jobs:
        if is_relevant(job):
            message = build_message(job)
            await notifier.send_job(job, message)
            sent_count += 1
    await update.message.reply_text(f"נשלחו {sent_count} משרות חדשות!")


CHOOSING = 1
JOB_TITLES = {
    1: "data 🗄️",
    2: "analyst 📊",
    3: "scientist 🔬",
    4: "machine learning 🤖",
    5: "ml 🤖",
    6: "bi 📈",
    7: "data labeling 🏷️",
    8: "data tagging 🏷️"
}

async def specific_jobs_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["all_choice"] = []
    text = "Choose a job title (send number, 0 to stop):\n"
    for k, v in JOB_TITLES.items():
        text += f"{k}️⃣ {v}\n"
    text += "0️⃣ Stop 🛑"
    await update.message.reply_text(text)
    return CHOOSING

# -------------------------------
# טיפול בהודעות המשתמש בבחירה
# -------------------------------
async def handle_specific_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # יציאה מהבחירה
    if text == "0":
        selections = context.user_data.pop("all_choice")
        await update.message.reply_text("✅ Your selections:\n" + "\n".join(selections))



        # הסרת האימוג'ים לחיפוש
        clean_titles = [s.split(" ")[0] for s in selections]

        await update.message.reply_text("🔍 Searching jobs for:\n" + ", ".join(clean_titles))

        jobs = fetch_jobs(keywords="data", location="Israel")
        relevant_jobs = []

        for job in jobs:
            title = job["title"].lower()
            if any(word.lower() in title for word in clean_titles):
                relevant_jobs.append(job)
        print(relevant_jobs)
        if relevant_jobs:
            message_text = "📋 Relevant jobs found:\n\n"
            for i, job in enumerate(relevant_jobs, start=1):
                message_text += f"{i}. {job['title']} - {job['company']}\n"
                message_text += f"   🔗 {job['link']}\n\n"
        else:
            message_text = "⚠️ No relevant jobs found for your selection."

            # שליחה למשתמש
        await update.message.reply_text(message_text)

        return ConversationHandler.END

        # בדיקה אם המספר תקין
    if not text.isdigit() or int(text) not in JOB_TITLES:
        await update.message.reply_text("⚠️ Send a number between 1–8 or 0")
        return CHOOSING

        # הוספת הבחירה
    choice = int(text)
    value = JOB_TITLES[choice]
    context.user_data["all_choice"].append(value)
    await update.message.reply_text(f"➕ Added: {value}")
    return CHOOSING








###########
    ######

    # בדיקה אם המספר תקין
    if not text.isdigit() or int(text) not in JOB_TITLES:
        await update.message.reply_text("⚠️ Send a number between 1–8 or 0")
        return CHOOSING

    # הוספת הבחירה
    choice = int(text)
    value = JOB_TITLES[choice]
    context.user_data["all_choice"].append(value)
    await update.message.reply_text(f"➕ Added: {value}")
    return CHOOSING

# פקודת /hello
async def hello_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "👋 Hello! Welcome to the Job Bot.\n\n"
        "Available commands:\n"
        "1️⃣ /1 - Get all relevant jobs\n"
        "2️⃣ /2 - Choose specific jobs by interest\n"
        "3️⃣ /3 - This screen, info and instructions\n\n"
        "To start, type the number of the command you want or click the command."
    )
    await update.message.reply_text(message)

# בניית האפליקציה
app = ApplicationBuilder().token(TOKEN).build()

# ConversationHandler עבור הבחירה
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("2", specific_jobs_command)],
    states={
        CHOOSING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_specific_choice)]
    },
    fallbacks=[]
)

# הוספת הפקודות
app.add_handler(CommandHandler("1", jobs_command))
app.add_handler(conv_handler)
app.add_handler(CommandHandler("3", hello_command))


print("Bot is running...")
app.run_polling()