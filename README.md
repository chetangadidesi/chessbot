# Chess Robot Arm Project

This project enables a robotic arm to play chess with a human opponent. It uses a chess engine (Stockfish) for move generation and an Arduino-controlled robotic arm to physically move the chess pieces.

---

## Features

- **Robotic Chess Arm**: Moves chess pieces on a real chessboard.
- **Stockfish Chess Engine**: Powers the AI to play challenging games.
- **Reach Validation**: Ensures moves are physically reachable by the robotic arm.
- **Inverse Kinematics**: Calculates arm angles to move to specific board positions.
- **Interactive Gameplay**: Play as Black while the computer plays as White.

---

## Requirements

### Hardware
- Robotic arm compatible with Arduino.
- Physical chessboard.

### Software
- Python 3.8 or higher.
- Arduino with serial communication enabled.
- Stockfish chess engine.

### Python Dependencies
- `python-chess`
- `pyserial`

---

## Setup

1. **Install Python Dependencies**:
   ```bash
   pip install python-chess pyserial
2. **Download Stockfish**:

    Obtain the Stockfish binary from Stockfish's official site.
    Place the binary in the project directory and update its path in game_update.py.
    Connect and Configure the Robotic Arm:

3. **Upload the Arduino code to the microcontroller using the Arduino IDE**.
    Update the port variable in armupdate.py to match the Arduino's COM port (e.g., COM5 or /dev/ttyUSB0).
    Calibrate the Chessboard:

4. **Measure and map the center coordinates of each square on the chessboard**.
    Update the square_coordinates dictionary in the Python scripts.

---

## Usage

1. **Run the main script - execute the command**:
   ```bash
   python game_update.py
2. **Play the Game**:

    Human Turn: Enter your move in UCI format (e.g., e2e4 for moving a pawn from e2 to e4).
    Robot Turn: The robotic arm will move the piece based on the move calculated by Stockfish.

3. **Game Ends**:

    Checkmate
    Stalemate
    Draw by insufficient material

## Customization

1. **Chessboard Dimensions**: Update the square_coordinates dictionary in the script to match your chessboard's layout.

2. **Arm Movement Speed**: Modify the speed parameter in the move_to_square function to control the arm's movement speed.

3. **Playing Difficulty**: Adjust the depth of Stockfish analysis in game_update.py by modifying the depth parameter.


## Troubleshooting:

1. **Arm Fails to Move to Correct Position**:
    Recheck the calibration of square_coordinates.
    Ensure the robotic arm's range covers all chessboard squares.
2. **Serial Communication Issues**:
    Verify the Arduino is properly connected and the correct COM port is specified.
    Restart the script if the connection drops.
3. **Invalid Moves**:
    Ensure moves are entered in valid UCI format.
    Check the game state for legal moves.
4. **Chessboard Misalignment**:
    Confirm the physical chessboard matches the square_coordinates mapping.


## Future Improvements:

1. **Vision System**: Implement a camera-based system to detect piece positions dynamically.
2. **Advanced Movement Algorithms**: Improve pathfinding to avoid collisions and optimize movement.


## Contributing:
**We welcome contributions to enhance the project! Here's how you can contribute**:

1. Fork the repository.
2. Create a feature branch: git checkout -b feature-name.
3. Commit your changes: git commit -m "Add a new feature".
4. Push to the branch: git push origin feature-name.
5. Open a pull request.



