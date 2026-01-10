# 🎲 Bingo Team Game - Excel VBA

An interactive, automated version of the classic 1-100 Bingo game built using Excel and VBA. This project is designed for classroom activities, team-building sessions, or group events, allowing for a seamless competition between two teams.

![Bingo Game Preview](https://github.com/saharYaccov/portfolio/blob/main/Excel%20%2B%20Vba/Bingo/image/image_1.jpeg?raw=true)

---

![Bingo Game Preview](https://github.com/saharYaccov/portfolio/blob/main/Excel%20%2B%20Vba/Bingo/image/image_2.jpeg?raw=true)

---

![Bingo Game Preview](https://github.com/saharYaccov/portfolio/blob/main/Excel%20%2B%20Vba/Bingo/image/image_3.png?raw=true)

## 📋 About the Project
The game features a 100-number grid where numbers are randomly drawn for two teams ("Team A" and "Team B"). The system automatically marks the board with the team's specific color, tracks history to prevent duplicate draws, and provides a clean user interface.

### Key Features:
* **Dual Team Management:** Separate "Spin" buttons for Team A and Team B.
* **Duplicate Prevention:** Utilizes VBA Collections to ensure every number is drawn only once.
* **Live History Log:** Real-time display of all "Numbers Drawn" to keep track of the game progress.
* **One-Click Reset:** A dedicated Reset button that clears the board, wipes the collection, and restores the UI.
* **Dynamic Styling:** Custom VBA scripts to remove gridlines, apply borders, and manage cell colors dynamically.

## 🚀 How to Play
1. Open the Excel file and **Enable Macros**.
2. Click the **RESET** button to initialize the board and clear any previous data.
3. Teams take turns clicking their respective **Spin** buttons.
4. The system will draw a number, highlight it on the board in the team's color, and add it to the history list.
5. The first team to complete a pattern or reach the goal (as defined by the moderator) wins!

## 🛠️ Technology Stack
* **Microsoft Excel**
* **VBA (Visual Basic for Applications)** - Core logic, randomization, and UI manipulation.
* **Collections** - Backend data structure for efficient number tracking.

## 🛠️ Technical Implementation (VBA)

The core of the game is driven by several key functions that handle the UI, randomization, and data integrity.

### 1. Board Initialization & Cleanup
* **`InitializeGame`**: Sets the stage by coloring the entire sheet background (`RGB 166, 201, 236`) and defining the 10x10 game board area (`RGB 125, 201, 239`) with black borders.
* **`ClearNumbersCollection`**: Re-initializes the global `nums` collection and clears the history display in cell **H13**.
* **`cleanCell`**: A utility used during animation to revert a cell's color back to the default board blue (`RGB 125, 201, 239`).

### 2. Randomization & Animation ("Spin" Logic)
The functions **`randNum`** and **`randNumTeam2`** create a visual "spinning" effect:
* **Animation Loop**: They iterate multiple times (`numIterLast`), showing temporary numbers on the board before landing on the final result.
* **`WaitSeconds`**: Provides a short delay (0.1s) and uses `DoEvents` to ensure the screen refreshes, allowing players to see the numbers changing in real-time.
* **Duplicate Protection**: A `Do While` loop combined with `checkIn` and `IsInNums` ensures the final number hasn't been drawn in the current game.

### 3. Team Styling & Highlights
* **`setColor` (Team 1)**: Highlights the winning cell using a solid theme color (Grey/Dark shade).
* **`setColorTeam2` (Team 2)**: Uses a **Linear Gradient** with a bright Orange color (`RGB 255, 165, 0`) to clearly distinguish Team 2's territory.

### 4. Data Validation & UI Updates
* **`checkIn` & `IsInNums`**: Methods used to verify if a generated number already exists in the `Public nums As Collection`.
* **`PrintCollectionToCell`**: Updates cell **H13** with a comma-separated list of every number stored in the collection.
* **`checkNext`**: Dynamically injects an Excel formula to perform a secondary validation check.

## 📂 Global Variables
```vba
Public nums As Collection ' Stores all drawn numbers to ensure uniqueness throughout the session.
```

🚀 How to Run

1. Open the Excel file and **Enable Macros**.
2. Click the **RESET** button to initialize the board and clear any previous data.
3. Teams take turns clicking their respective **Spin** buttons.
4. The system will draw a number, highlight it on the board in the team's color, and add it to the history list.
5. The first team to complete a pattern or reach the goal (as defined by the moderator) wins!

---

##10-JAN-26 Developed by [Sahar Yaccov](https://github.com/saharYaccov).
