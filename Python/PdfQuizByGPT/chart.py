'''
This script generates a right-to-left aligned PDF quiz in Hebrew (or RTL-compatible languages),
based on structured multiple-choice questions and answers written in plain text.

Core Features:
--------------
1. Automatically detects numbered questions (e.g., "1. Question") and transforms them into
   a structured format using `parse_questions()`.

2. Adds a pipe character ('|') after each question number using `add_pipe_after_number()`
   for consistent formatting and splitting.

3. Uses the ReportLab library to:
   - Generate a PDF file (A4 size) with RTL text alignment.
   - Support custom Hebrew fonts (e.g., Arial.ttf).
   - Automatically wrap long quizzes across multiple pages.
   - Align all text rightward using `bidi` and `arabic_reshaper` for proper Hebrew/Arabic layout.

Main Functions:
---------------
- reshape_rtl(text): Reshapes and reorders RTL strings for proper PDF display.
- parse_questions(text): Parses plain text into a list of questions and answers.
- add_pipe_after_number(text): Ensures formatting consistency for question numbering.
- create_pdf_from_questions(questions, filename): Renders all questions/answers into a clean PDF.

Dependencies:
-------------
- reportlab
- bidi
- arabic_reshaper

Font Requirement:
-----------------
Make sure you have 'Arial.ttf' (or another Hebrew-supported font) in your working directory.
You may replace `'Arial.ttf'` with another suitable font file if needed.

Output:
-------
Generates a well-formatted PDF quiz (default: "quiz.pdf" or a custom title), for example:
✔ PDF נוצר בהצלחה: quiz - History, Science, and Beverages.pdf

@author: Sahar
'''



from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from bidi.algorithm import get_display
import arabic_reshaper

# הרשמת פונט עברי – שים לב לשם הקובץ שיש לך בתיקייה
pdfmetrics.registerFont(TTFont('Hebrew', 'Arial.ttf'))  # ודא שהפונט קיים בתיקייה או החלף לפונט שיש לך

def reshape_rtl(text):
    reshaped_text = arabic_reshaper.reshape(text)
    return get_display(reshaped_text)

def parse_questions(text):
    """
    מקבלת מחרוזת טקסט עם פורמט שבו שאלות מופרדות ב-.| ותשובות אחרי ?
    מחזירה רשימה של מילונים עם מפתח 'question' ו-'answers' (רשימת תשובות)
    """
    results = []
    parts = text.split(".|")
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if '?' in part:
            question_part, answers_part = part.split('?', 1)
            question = question_part.strip() + '?'
            answers = [a.strip() for a in answers_part.strip().split('\n') if a.strip()]
        else:
            question = part
            answers = []
        results.append({'question': question, 'answers': answers})
    return results

def create_pdf_from_questions(questions, filename="quiz.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    c.setFont("Hebrew", 12)

    width, height = A4
    margin = 50
    line_height = 20
    y = height - margin

    nextPage = 0
    for i, qa in enumerate(questions, 1):
        question_text = reshape_rtl(f"{i}. {qa['question']}")
        c.drawRightString(width - margin, y, question_text)
        y -= line_height

        for answer in qa['answers']:
            answer_text = reshape_rtl(answer)
            c.drawRightString(width - margin - 10, y, answer_text)
            y -= line_height * 0.9

        y -= line_height * 0.5  # רווח נוסף אחרי כל שאלה

        # מעבר עמוד אם אין מקום
        if y < margin:
            c.showPage()
            c.setFont("Hebrew", 12)
            y = height - margin
        if nextPage%4==0 and nextPage!=0:
            c.showPage()
            c.setFont("Hebrew", 12)
            y = height - margin
        nextPage+=1
    c.save()
    print(f"✔ PDF נוצר בהצלחה: {filename}")
import re

import re

def add_pipe_after_number(text):
    """
    מוסיפה את הסימן '|', אחרי מספר בתחילת שורה שמסתיים בנקודה.
    לדוגמה: '1. שאלה' -> '1.| שאלה'
    """
    # משתמשים ב־regex לזיהוי מספר בתחילת שורה שמסתיים בנקודה
    return re.sub(r'^(\d+)\.', r'\1.|', text, flags=re.MULTILINE)

text = '''
1. Who was the first President of the United States?  
A. Thomas Jefferson  
B. George Washington  
C. Benjamin Franklin  
D. Abraham Lincoln  

Answer: B. George Washington

2. What is the chemical formula of water?  
A. CO2  
B. H2O  
C. O2  
D. CH4  

Answer: B. H2O

3. Which traditional drink is made from grapes?  
A. Beer  
B. Whiskey  
C. Wine  
D. Rum  

Answer: C. Wine

4. When did the French Revolution take place?  
A. 1492  
B. 1789  
C. 1914  
D. 1945  

Answer: B. 1789

5. Who discovered the laws of motion and gravity?  
A. Albert Einstein  
B. Isaac Newton  
C. Galileo Galilei  
D. Marie Curie  

Answer: B. Isaac Newton

6. What is the national drink of Mexico?  
A. Tequila  
B. Whiskey  
C. Cider  
D. Cognac  

Answer: A. Tequila

7. In which year did the first man land on the moon?  
A. 1969  
B. 1955  
C. 1975  
D. 1980  

Answer: A. 1969

8. Which chemical element has the symbol Fe?  
A. Copper  
B. Gold  
C. Iron  
D. Silver  

Answer: C. Iron

9. What is the main drink made from corn in the United States?  
A. Rum  
B. Whiskey  
C. Vodka  
D. Gin  

Answer: B. Whiskey

10. Who was the emperor of the Roman Empire at the fall of Rome?  
A. Julius Caesar  
B. Augustus  
C. Romulus Augustulus  
D. Trajan  

Answer: C. Romulus Augustulus

11. What is the capital city of Australia?  
A. Sydney  
B. Melbourne  
C. Canberra  
D. Brisbane  

Answer: C. Canberra

12. Who wrote "Romeo and Juliet"?  
A. Charles Dickens  
B. William Shakespeare  
C. Jane Austen  
D. Mark Twain  

Answer: B. William Shakespeare

13. What is the largest planet in our solar system?  
A. Earth  
B. Mars  
C. Jupiter  
D. Saturn  

Answer: C. Jupiter

14. Which language is primarily spoken in Brazil?  
A. Spanish  
B. Portuguese  
C. French  
D. English  

Answer: B. Portuguese

15. What is the boiling point of water at sea level in Celsius?  
A. 100  
B. 90  
C. 80  
D. 110  

Answer: A. 100

16. Who painted the Mona Lisa?  
A. Vincent Van Gogh  
B. Pablo Picasso  
C. Leonardo da Vinci  
D. Michelangelo  

Answer: C. Leonardo da Vinci

17. Which country is known as the Land of the Rising Sun?  
A. China  
B. South Korea  
C. Japan  
D. Thailand  

Answer: C. Japan

18. What is the hardest natural substance on Earth?  
A. Gold  
B. Diamond  
C. Quartz  
D. Iron  

Answer: B. Diamond

19. How many continents are there?  
A. 5  
B. 6  
C. 7  
D. 8  

Answer: C. 7

20. What gas do plants absorb from the atmosphere?  
A. Oxygen  
B. Nitrogen  
C. Carbon dioxide  
D. Helium  

Answer: C. Carbon dioxide

21. Who is known as the Father of Computers?  
A. Alan Turing  
B. Charles Babbage  
C. Steve Jobs  
D. Bill Gates  

Answer: B. Charles Babbage

22. What is the tallest mountain in the world?  
A. K2  
B. Kangchenjunga  
C. Mount Everest  
D. Lhotse  

Answer: C. Mount Everest

23. Which organ pumps blood through the body?  
A. Liver  
B. Kidney  
C. Heart  
D. Lung  

Answer: C. Heart

24. What is the main ingredient in traditional Japanese sushi?  
A. Bread  
B. Rice  
C. Cheese  
D. Pasta  

Answer: B. Rice

25. Who was the first woman to win a Nobel Prize?  
A. Marie Curie  
B. Rosalind Franklin  
C. Ada Lovelace  
D. Jane Goodall  

Answer: A. Marie Curie

26. What is the currency of the United Kingdom?  
A. Euro  
B. Dollar  
C. Pound Sterling  
D. Yen  

Answer: C. Pound Sterling

27. Which planet is closest to the Sun?  
A. Venus  
B. Earth  
C. Mercury  
D. Mars  

Answer: C. Mercury

28. What is the chemical symbol for gold?  
A. Au  
B. Ag  
C. Gd  
D. Go  

Answer: A. Au

29. Which famous scientist developed the theory of relativity?  
A. Nikola Tesla  
B. Isaac Newton  
C. Albert Einstein  
D. Galileo Galilei  

Answer: C. Albert Einstein

30. What is the largest ocean on Earth?  
A. Atlantic  
B. Indian  
C. Pacific  
D. Arctic  

Answer: C. Pacific

31. Who wrote "1984" and "Animal Farm"?  
A. J.K. Rowling  
B. George Orwell  
C. Ernest Hemingway  
D. F. Scott Fitzgerald  

Answer: B. George Orwell

32. Which country gifted the Statue of Liberty to the USA?  
A. England  
B. France  
C. Germany  
D. Spain  

Answer: B. France

33. What is the primary language spoken in Canada?  
A. English and French  
B. Spanish  
C. English only  
D. French only  

Answer: A. English and French

34. What is the largest desert in the world?  
A. Sahara  
B. Gobi  
C. Antarctic Desert  
D. Arabian  

Answer: C. Antarctic Desert

35. Who discovered penicillin?  
A. Marie Curie  
B. Alexander Fleming  
C. Louis Pasteur  
D. Jonas Salk  

Answer: B. Alexander Fleming

36. Which element has the atomic number 1?  
A. Helium  
B. Oxygen  
C. Hydrogen  
D. Nitrogen  

Answer: C. Hydrogen

37. What is the capital of Egypt?  
A. Alexandria  
B. Cairo  
C. Giza  
D. Luxor  

Answer: B. Cairo

38. Which city hosted the 2012 Summer Olympics?  
A. Beijing  
B. Rio de Janeiro  
C. London  
D. Tokyo  

Answer: C. London

39. What is the smallest prime number?  
A. 0  
B. 1  
C. 2  
D. 3  

Answer: C. 2

40. Who painted the ceiling of the Sistine Chapel?  
A. Leonardo da Vinci  
B. Michelangelo  
C. Raphael  
D. Donatello  

Answer: B. Michelangelo

41. Which country is famous for the Taj Mahal?  
A. Pakistan  
B. India  
C. Bangladesh  
D. Nepal  

Answer: B. India

42. What is the main gas found in the Earth's atmosphere?  
A. Oxygen  
B. Nitrogen  
C. Carbon dioxide  
D. Hydrogen  

Answer: B. Nitrogen

43. What is the process by which plants make food?  
A. Respiration  
B. Photosynthesis  
C. Transpiration  
D. Fermentation  

Answer: B. Photosynthesis

44. Who is the author of "The Catcher in the Rye"?  
A. J.D. Salinger  
B. Harper Lee  
C. Mark Twain  
D. John Steinbeck  

Answer: A. J.D. Salinger

45. What is the square root of 64?  
A. 6  
B. 7  
C. 8  
D. 9  

Answer: C. 8

46. Which metal is liquid at room temperature?  
A. Mercury  
B. Lead  
C. Copper  
D. Zinc  

Answer: A. Mercury

47. What is the longest river in the world?  
A. Amazon  
B. Nile  
C. Yangtze  
D. Mississippi  

Answer: B. Nile

48. Who invented the telephone?  
A. Nikola Tesla  
B. Thomas Edison  
C. Alexander Graham Bell  
D. Guglielmo Marconi  

Answer: C. Alexander Graham Bell

49. Which planet is known as the Red Planet?  
A. Venus  
B. Mars  
C. Jupiter  
D. Saturn  

Answer: B. Mars

50. What is the powerhouse of the cell?  
A. Nucleus  
B. Ribosome  
C. Mitochondria  
D. Chloroplast  

Answer: C. Mitochondria

'''
title = 'quiz - History, Science, and Beverages.pdf'

processed_text = add_pipe_after_number(text)



parsed = parse_questions(processed_text)           # שלב 1: הפיכת טקסט לרשימת שאלות
create_pdf_from_questions(parsed,filename=title)        # שלב 2: יצירת PDF
