# 🎮 המשחק שלי

ברוכים הבאים לפרויקט שלי! כאן תמצאו את כל ההוראות להתקנת Python, התקנת תלויות, ניווט לתיקיית הפרויקט והרצת המשחק.

> **[English README - Click Here ](https://github.com/saharYaccov/portfolio/blob/main/Freedom-Force-The-Reckoning/READMEEM.md)**

--

> **![Game Demo](https://github.com/saharYaccov/portfolio/blob/main/Freedom-Force-The-Reckoning/Gif/gameVideo0.gif)**
> **![Game Demo](https://github.com/saharYaccov/portfolio/blob/main/Freedom-Force-The-Reckoning/Gif/gameVideo1.gif)**
## 🖥 דרישות מוקדמות

- מחשב עם מערכת הפעלה **Windows / macOS / Linux**
- חיבור לאינטרנט
- קובץ המשחק (`main.py`) ותיקיית פרויקט נקייה

---

## 1️⃣ התקנת Python

1. הורידו את Python מהאתר הרשמי: [הורדת Python](https://www.python.org/downloads/)
2. במהלך ההתקנה, **וודאו שסימנתם את התיבה "Add Python to PATH"**
3. השלימו את תהליך ההתקנה

כדי לוודא ש-Python הותקן בצורה נכונה, הריצו את הפקודה הבאה בטרמינל (או במסוף) :

```bash
python --version
```
או
```bash
python3 --version
```

---

## 2️⃣ התקנת תלויות

פתחו את הטרמינל (שורת פקודה ב-Windows, טרמינל ב-macOS/Linux).

התקינו את הספריות הנדרשות למשחק. לדוגמה, אם המשחק שלכם משתמש ב-**Pygame**, הריצו:

```bash
pip install pygame
pip install numpy
pip install pandas
```

💡 **טיפ:** אם המשחק שלכם משתמש במספר ספריות, צרו קובץ בשם `requirements.txt` עם רשימת הספריות (ספריה אחת בכל שורה), לדוגמה (קיים בתקיית הפרויקט ):

```
pygame
numpy
pandas
```
עברו לנתיב של הפרויקט ( של Freedom-Force-The-Reckoning-game במחשב שלכם )
ואז הריצו את הפקודה הבאה כדי להתקין את כל הספריות בפעם אחת:

```bash
pip install -r requirements.txt
```

---

## 3️⃣ ניווט לתיקיית הפרויקט

העבירו את עצמכם לתיקיית הפרויקט באמצעות הפקודה:

```bash
cd נתיב/לתיקיית/המשחק/שלכם
```

לדוגמה, אם תיקיית המשחק נמצאת על שולחן העבודה:

```bash
cd Desktop/MyGame
```

---

## 4️⃣ הרצת המשחק

הריצו את קובץ המשחק באמצעות הפקודה:

```bash
python game.py
```
או
```bash
python3 game.py
```

---

## 5️⃣ אופציונלי: שימוש בסביבת פיתוח וירטואלית

כדי ליצור סביבה מבודדת לפרויקט, הריצו:

```bash
python -m venv venv
```

הפעילו את הסביבה הווירטואלית לפי מערכת ההפעלה שלכם:

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

לאחר ההפעלה, התקינו את כל התלויות בתוך הסביבה הווירטואלית:

```bash
pip install -r requirements.txt
```

---

אחרי שהגעתם לנתיב הפרויקט, הריצו את קובץ main.py:
```bash
python main.py
```
or
```bash
python3 main.py
```

---
