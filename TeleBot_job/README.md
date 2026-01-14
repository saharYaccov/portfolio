dsשמעולה, הנה **הגרסה המלאה – באנגלית בלבד – כ־Raw Markdown בתוך בלוק קוד**, מוכן להעתקה אחד־לאחד 👇
# **Telegram Job Bot – Full Step-by-Step Guide**

This document describes a **complete end-to-end process** for creating, configuring, and running a Telegram bot
that scrapes job postings, filters them, and sends notifications to a Telegram chat.

---

## **📁 Project Structure**

```

.
├── bot/
├── data/
├── filters/
├── generator/
├── scraper/
├── video/
│   └── video1.mp4
├── commant.py
├── detail.json
├── main.py
├── requirements.txt
├── telegram_url.md
├── test_telebot_job.py

````

---

## **🧩 Folder and File Overview**

### **bot/**
Handles all **Telegram-related functionality**:
- Sending messages to Telegram chats
- Communicating with the Telegram Bot API
- Managing the notifier / sender logic

---

### **data/**
Stores **static and dynamic data**:
- Keyword lists
- JSON configuration or cache files
- Data persisted between executions

---

### **filters/**
Contains **job filtering logic**:
- Matching job titles against keywords
- Excluding unwanted roles (e.g., Senior, Lead, Principal)
- Determining job relevance

---

### **generator/**
Responsible for **message generation**:
- Building formatted job messages
- Preparing content for Telegram delivery
- Combining job title, company name, and URLs

---

### **scraper/**
Handles **job data collection** from external sources:
- Job boards (e.g., LinkedIn)
- `fetch_jobs` and scraping logic

---

### **commant.py**
**Main execution entry point** of the project:
- Listens for bot commands or triggers
- Executes the job scraping pipeline
- Sends job notifications to Telegram

---

### **detail.json**
Sensitive configuration file (**do not upload real values to GitHub**):

```json
{
  "TOKEN": "YOUR_TELEGRAM_BOT_TOKEN",
  "CHAT_ID": "YOUR_TELEGRAM_CHAT_ID"
}
````

Required values:

* `TOKEN` – Telegram Bot token received from BotFather
* `CHAT_ID` – Telegram chat ID where messages will be sent

---

### **main.py**

Core application logic:

* Connects scraper → filters → generator → bot

---

### **requirements.txt**

List of Python dependencies:

```
python-telegram-bot
requests
beautifulsoup4
```

Install dependencies using:

```
pip install -r requirements.txt
```

---

### **telegram_url.md**

Documentation file:

* Bot URLs
* Available commands
* Usage notes

---

### **test_telebot_job.py**

Testing utilities:

* Message sending tests
* Job filtering validation

---

## **🤖 Bot Setup – Step by Step**

### **1️⃣ Create a Telegram Bot**

1. Open Telegram
2. Search for **BotFather**
3. Send `/start`
4. Send `/newbot`
5. Choose a name for your bot
6. Copy and save the generated **BOT TOKEN**

---

### **2️⃣ Retrieve Your CHAT_ID**

You can obtain your chat ID using one of the following methods:

* Send a message to your bot and call `getUpdates`
* Use the Telegram bot **@userinfobot**

---

### **3️⃣ Configure detail.json**

Replace placeholders with your actual values:

```json
{
  "TOKEN": "123456:ABCDEF",
  "CHAT_ID": "5279346740"
}
```

---

### **4️⃣ Install Dependencies**

Create and activate a virtual environment (recommended):

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### **5️⃣ Run the Bot**

Start the bot by running:

```
python commant.py
```

Once running, the bot will begin scraping jobs and sending notifications 🎉

---

## **🎬 Demo Video**

A demo video is included in the following path:

```
video/video1.mp4
```

The video demonstrates:

* Bot startup
* Job scraping process
* Message delivery to Telegram

---

## **✅ Summary**

* Clean and modular project structure
* Easy to maintain and extend
* Suitable for automated job searching and notifications

  <video width="800" controls>
  <source src="https://github.com/saharYaccov/portfolio/raw/main/TeleBot_job/video/video1.mp4" type="video/mp4">
  Your browser does not support the video tag.
</video>


