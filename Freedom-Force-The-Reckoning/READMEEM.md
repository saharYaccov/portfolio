# 🎮 My Game

Welcome to my project! Here you will find all the instructions to install Python, set up dependencies, navigate to the project folder, and run the game.

> **[Hebrew version of this file](https://github.com/saharYaccov/portfolio/blob/main/Freedom-Force-The-Reckoning/READMEEM.md)**
---

## 🎬 Game Demo

> **![Game Demo](https://github.com/saharYaccov/portfolio/blob/main/Freedom-Force-The-Reckoning/Gif/gameVideo0.gif)**
---

## 🖥 Prerequisites

- A computer with **Windows / macOS / Linux**
- Internet connection
- Your game file (`game.py`) and a clean project folder

---

## 1️⃣ Install Python

1. Download Python from the official website: [Python Downloads](https://www.python.org/downloads/)
2. During installation, **make sure to check the box "Add Python to PATH"**
3. Complete the installation process

To verify that Python is installed correctly, run the following command in the terminal:

```bash
python --version
```
or
```bash
python3 --version
```

---

## 2️⃣ Install Dependencies

Open the terminal (Command Prompt on Windows, Terminal on macOS/Linux).

Install the required libraries for the game. For example, if your game uses **Pygame**, run:

```bash
pip install pygame
```

💡 **Tip:** If your game uses multiple libraries, create a file named `requirements.txt` with one library per line, for example:

```
pygame
numpy
pandas
```

Then run the following command to install all the libraries at once:

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Navigate to the Project Folder

Move to your project folder using the command:

```bash
cd path/to/your/game/folder
```

For example, if your game folder is on the desktop:

```bash
cd Desktop/MyGame
```

---

## 4️⃣ Run the Game

Run the game file using the command:

```bash
python game.py
```
or
```bash
python3 game.py
```

---

## 5️⃣ Optional: Using a Virtual Environment

To create an isolated environment for the project, run:

```bash
python -m venv venv
```

Activate the virtual environment according to your operating system:

**macOS / Linux:**

```bash
source venv/bin/activate
```

**Windows:**

```bash
venv\Scripts\activate
```

After activation, install all dependencies inside the virtual environment:

```bash
pip install -r requirements.txt
```

---
