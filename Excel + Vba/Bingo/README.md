# 🎲 Bingo Team Game - Excel VBA

An interactive, automated version of the classic 1-100 Bingo game built using Excel and VBA. This project is designed for classroom activities, team-building sessions, or group events, allowing for a seamless competition between two teams.

![Bingo Game Preview](https://github.com/saharYaccov/portfolio/blob/main/Excel%20%2B%20Vba/Bingo/image/image_1.jpeg?raw=true)

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

## 📂 Code Structure
* `InitializeGame`: Sets up the workspace, colors the entire sheet, and draws the board borders.
* `SpinTeamButton_Click`: The main logic for drawing a random number and updating the game state.
* `ShowChosenNumbers`: Iterates through the collection to display the history string in a specific cell.
* `cleanCell`: A utility function to restore a cell's color by sampling the background (using `ActiveCell` or `RGB`).

---
Developed by [Sahar Yaccov](https://github.com/saharYaccov).
