# GalaxyLife Bot

This project is an automated system designed to streamline and optimize gameplay interactions through image processing
and GUI automation techniques as the game doesn't implement any API endpoints. It simulates player actions in a game
environment by identifying lucrative targets based on game visuals, engaging with enemies automatically, and managing
resources effectively. The system is designed to operate continuously, mainly focusing on gathering resources.

## Table of Contents

- [Introduction](#introduction)
- [Installation](#installation)
- [Usage](#usage)
- [Modules Description](#modules-description)
    - [Main Loop](#main-loop)
    - [Utilities Module](#utilities-module)
    - [Game Actions](#game-actions)
    - [Image Processing](#image-processing)
- [Technologies Used](#technologies-used)


## Introduction

This system is designed to automate repetitive tasks in the game "Galaxy Life," allowing for efficient management of
game actions such as searching for enemies, attacking them based on strategic analysis, and managing troop training. By
automating these tasks, players can focus on strategic decision-making and resource management.

## Installation

To get started with this project, follow these steps:

1. **Clone the repository:**
   ```bash
   git clone https://github.com/amdla/GalaxyLifeBot.git
   cd GalaxyLifeBot
   ```

2. **Install required libraries:**
   ```bash
   pip install -r requirements
   ```

3. **Setup environment:**
   Ensure that your game window is correctly configured as per the coordinates specified in the `utils.py`.
   You can adjust the coordinates within the file to match your base setup.
   Current version requires 2560x1440 resolution. It will hopefully be switched to unified Virtual Machine in the future.


## Usage

To run the automation script, execute the following command in the root directory after turning on the game:

```bash
python main.py
```

This will start the automation process, switch the window to the game, where the system will begin to search for enemies,
evaluate if they're worth attacking, and manage troop training cycles.

## Modules Description

### Main Loop

`main.py` is the entry point of the application. It initializes the system, sets up logging, and manages the main loop
which coordinates all actions:

- **Logging:** Configured to track the process flow and errors.
- **Excel Logging:** Captures and logs each action's outcome for later analysis.
- **Main Loop:** Orchestrates the game actions, maintaining continuous operation unless halted by manual intervention or
  a fatal error.

### Utilities Module

`utils.py` includes utility functions that facilitate the operations of game actions:

- **Directory Management:** Manages file directories for screenshots and logs.
- **Interaction Helpers:** Includes functions to simulate mouse clicks and keystrokes.
- **Error Handling:** Robust error handling mechanisms to ensure continuous operation.

### Game Actions

`game_actions.py` contains functions that directly interact with the game:

- **Enemy Search:** Automates the process of searching for new enemies.
- **Attack Management:** Handles the deployment of troops and manages attacks.
- **Troop Training:** Automates the queuing of troops for training post-attack.

### Image Processing

`image_processing.py` is crucial for analyzing game state from screenshots:

- **Screenshot Handling:** Captures and processes screenshots.
- **OCR Capabilities:** Uses OCR to extract numeric values from images.
- **Defensive Analysis:** Utilizes a trained model to decide the strategic value of attacking a specific enemy base.

## Technologies Used

- Python
- PyAutoGUI
- OpenCV
- EasyOCR
- PyTorch
- YOLO (You Only Look Once) for object detection
- Openpyxl for Excel operations
