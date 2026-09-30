# Lab 4: VibeCoding — AI-Assisted Pair Programming & Game Refactoring

**Student Name:** Ganavi Gowda  
**SRN:** PES1UG24CS707  
**Course:** Software Engineering Lab (PES University - Dept. of CSE)  
**Assigned System / Problem Statement #43:** Real-Time Reaction Time Tester (Pygame)  
**Personal Repository:** [ganavigowda8343-ctrl/43_reaction-time-tester](https://github.com/ganavigowda8343-ctrl/43_reaction-time-tester)  
**Starter Repository:** [SETAPESU26/43_reaction-time-tester](https://github.com/SETAPESU26/43_reaction-time-tester)  
**Reference Structure:** [kavanapg276-glitch/SE/tree/main/Lab-4](https://github.com/kavanapg276-glitch/SE/tree/main/Lab-4)  

---

## 📋 Table of Contents
1. [Lab Overview & Objectives](#-lab-overview--objectives)
2. [Deliverables Inventory](#-deliverables-inventory)
3. [Identified Bugs & Tasks Completed](#-identified-bugs--tasks-completed)
4. [Video Proof & Demonstrations](#-video-proof--demonstrations)
5. [AI Pair-Programming (VibeCoding) Chat History](#-ai-pair-programming-vibecoding-chat-history)
6. [How to Run the Updated Game](#-how-to-run-the-updated-game)

---

## 📌 Lab Overview & Objectives
The objective of this lab is to use an AI assistant (pair-programming / "VibeCoding" methodology) to analyze, debug, and extend a partially working Pygame reaction-time tester. The starter codebase contained timing bugs, lacked input validation during wait phases, had no post-game results screen or replay system, and lacked audio feedback cues.

Through iterative prompts with ChatGPT and critical code evaluations:
- The timing system was completely overhauled to measure reaction strictly from the green visual cue.
- False starts during the grey wait screen were intercepted and flagged.
- A post-game results screen calculating individual round scores and session average was implemented.
- An interactive replay system with difficulty options (Easy, Medium, Hard) was added.
- Dynamic sound feedback for "go", false starts, and session termination was integrated.

---

## 📦 Deliverables Inventory

| Deliverable | File / Directory | Description |
| :--- | :--- | :--- |
| **BEFORE Video** | [`before.mp4`](before.mp4) | Gameplay video recorded before modifications, clearly demonstrating the timing inflation bug and lack of false-start handling. |
| **AFTER Video** | [`after.mp4`](after.mp4) | Gameplay video recorded after changes, showing accurate reaction timing, false-start warning, results screen, and replay flow. |
| **Chat History (PDF)** | [`Chat_history.pdf`](Chat_history.pdf) | Compiled conversational transcript of the AI pair-programming session in ChatGPT. |
| **Chat History (Alt)** | [`Lab4_VibeCoding_Chat_History.pdf`](Lab4_VibeCoding_Chat_History.pdf) | Original compiled PDF export of the chat transcript. |
| **Chat Reference** | [`chat_link.txt`](chat_link.txt) | Metadata file documenting student, starter repo, and chat transcript references. |
| **Full Game Package** | [`reaction-time-tester/`](reaction-time-tester/) | Complete game directory containing `game/` engine, `main.py`, `requirements.txt`, and `README.md` (structured identically to `balloon-pop/` in reference repository). |
| **Updated Source Code** | [`updated-code/`](updated-code/) | Clean updated source code files (`main.py`, `requirements.txt`, `game/game_engine.py`, `game/round.py`). |

---

## 🛠️ Identified Bugs & Tasks Completed

### Task 1: Refine Input Timing Detection & False Start Handling
- **Original Bug**: In the starter code, reaction time was measured from when the round started rather than when the screen turned green. As a result, reaction times were inflated by the duration of the random wait phase, and clicking during the grey screen was incorrectly counted as a valid reaction.
- **Fix Implemented**:
  - `round.py` was refactored to separate the `WAITING` state from the `READY` state.
  - Reaction timer now starts strictly at the exact timestamp when the screen turns green.
  - Early clicks or spacebar presses during the grey screen are intercepted as **False Starts** and visually/audibly flagged.

### Task 2: Implement Game Over & Results Screen
- **Original Bug**: When rounds ended, results were merely printed to the console terminal, and the Pygame window abruptly closed.
- **Fix Implemented**:
  - Added a dedicated graphical results view in `game_engine.py`.
  - Displays each round's reaction time in milliseconds along with the overall average reaction time.
  - Provides clear visual hierarchy and waits for player input before advancing.

### Task 3: Add Replay Option & Difficulty Selection
- **Original Bug**: No replay loop existed; the program terminated immediately after one round sequence.
- **Fix Implemented**:
  - Implemented an interactive post-session menu allowing the player to replay or quit (`ESC`).
  - Added three difficulty presets configuring the wait intervals and cue predictability:
    - **Easy**: Longer cue window (2.0s – 5.0s wait)
    - **Medium**: Standard cue window (1.5s – 4.0s wait)
    - **Hard**: Short, twitch-reflex cue window (1.0s – 2.5s wait)

### Task 4: Add Sound Feedback
- **Original Bug**: The game was entirely silent with no auditory cues.
- **Fix Implemented**:
  - Integrated `pygame.mixer` synthesized audio cues for:
    1. **Go Cue**: High-frequency chime when the screen turns green.
    2. **False Start Cue**: Low-frequency warning buzz when clicked prematurely.
    3. **Session Complete Cue**: Completion tone upon reaching the results screen.

---

## 🎬 Video Proof & Demonstrations

1. **Before Changes (`before.mp4`)**:
   - Shows the game running with inflated reaction times.
   - Demonstrates pressing during the grey wait phase without false start penalties.
2. **After Changes (`after.mp4`)**:
   - Demonstrates the screen turning green and accurately recording reaction time.
   - Demonstrates the false-start detection and audio cues.
   - Demonstrates the final results screen displaying all times and the average.
   - Demonstrates the difficulty/replay menu.

---

## 💬 AI Pair-Programming (VibeCoding) Chat History
The full debugging and development conversation with the AI assistant (ChatGPT) is preserved in [`Chat_history.pdf`](Chat_history.pdf).

The chat logs demonstrate:
1. Environment setup and resolving Pygame compilation in macOS virtual environment (`python3.12 -m venv .venv`).
2. Iterative debugging of the timing calculation in `game/round.py`.
3. Architecture of the state machine in `game/game_engine.py` for results and replay.
4. Git branching, testing, and backup workflows to capture both the broken and fixed game states.

---

## 🚀 How to Run the Updated Game

### Prerequisites
- Python 3.10+ (tested on Python 3.12.14)
- `pygame` 2.6.1+

### Installation & Execution
```bash
# 1. Navigate to the game directory
cd Lab-4/reaction-time-tester

# 2. (Optional) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the game
python main.py
```

### Controls
- **Spacebar / Left Click**: React to green cue or select options.
- **1 / 2 / 3**: Select Easy / Medium / Hard difficulty on replay screen.
- **ESC**: Exit game.
