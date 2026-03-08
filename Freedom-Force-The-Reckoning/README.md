🔹 מדריך בעברית
דרישות מוקדמות

מחשב עם מערכת הפעלה Windows / macOS / Linux

חיבור לאינטרנט

קובץ המשחק שלך (game.py) ותיקיית פרויקט מסודרת

1️⃣ התקנת פייתון

הורד את פייתון מהאתר הרשמי: https://www.python.org/downloads/

במהלך ההתקנה סמן את האפשרות "Add Python to PATH".

סיים את ההתקנה.

כדי לבדוק שהפייתון הותקן בהצלחה:

python --version

או

python3 --version
2️⃣ התקנת תלותים (ספריות)

פתח טרמינל (Command Prompt ב-Windows, Terminal ב-macOS/Linux)

התקן את כל הספריות שהמשחק שלך צריך. לדוגמה, אם המשחק משתמש ב-pygame:

pip install pygame

אם יש לך יותר מספריות, אפשר להכין קובץ requirements.txt עם כל הספריות, ואז להריץ:

pip install -r requirements.txt
3️⃣ ניווט לתיקיית המשחק
cd נתיב/לתיקיית/המשחק

לדוגמה:

cd Desktop/MyGame
4️⃣ הפעלת המשחק
python game.py

או

python3 game.py
5️⃣ טיפים

אם יש לך בעיות בהרצה, ודא שהגרסה של פייתון תואמת לגרסה שבה נכתב הקוד.

אם רוצים, אפשר ליצור סביבה וירטואלית לפני התקנת הספריות:

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
