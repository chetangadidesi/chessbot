# Play a chess game without using Computer Vision

import chess
import chess.engine
from armupdate import ChessRobotArm
import random

# Initialize the chess engine (Stockfish)
engine = chess.engine.SimpleEngine.popen_uci(
    r"C:\\Users\\cheta\\Downloads\\ChessRobotArm-master (2)\\ChessRobotArm-master\\ChessRobotArm-master\\stockfish\\stockfish-windows-2022-x86-64-avx2.exe"
)

# Initialize the board and robotic arm
board = chess.Board()
robot = ChessRobotArm(port='COM5', verbose=True)  # Connect to Arduino via COM6

# Define chessboard coordinates (update as needed for full board)

#square_coordinates = {
 #  'a1': (0, 0, 12),
 #  'h1': (28, 0, 12),
    # 'e2': (16, 12, 12),
#    'e4': (16, 12, 12),
 #   'd4': (16, 14, 12),
  #  'f3': (13, 8, 12),
  #  'e3': (13, 12, 12),
 #   'd3': (13, 14, 12),
    # Add the remaining squares here
  #  'discard': (35, 35, 12),  # Example discard square for captured pieces
#}


square_coordinates = {
    'a1': (6, 23, 12), 'b1': (6, 20, 12), 'c1': (6, 17, 12), 'd1': (6, 14, 12),
    'e1': (6, 11, 12), 'f1': (6, 8, 12), 'g1': (6, 5, 12), 'h1': (6, 2, 12),
    'a2': (9, 23, 12), 'b2': (9, 20, 12), 'c2': (9, 17, 12), 'd2': (9, 14, 12),
    'e2': (9, 11, 12), 'f2': (9, 8, 12), 'g2': (9, 5, 12), 'h2': (9, 2, 12),
    'a3': (12, 23, 12), 'b3': (12, 20, 12), 'c3': (12, 17, 12), 'd3': (12, 14, 12),
    'e3': (12, 11, 12), 'f3': (12, 8, 12), 'g3': (12, 5, 12), 'h3': (12, 2, 12),
    'a4': (15, 23, 12), 'b4': (15, 20, 12), 'c4': (15, 17, 12), 'd4': (15, 14, 12),
    'e4': (15, 11, 12), 'f4': (15, 8, 12), 'g4': (15, 5, 12), 'h4': (15, 2, 12),
    'a5': (18, 23, 12), 'b5': (18, 20, 12), 'c5': (18, 17, 12), 'd5': (18, 14, 12),
    'e5': (18, 11, 12), 'f5': (18, 8, 12), 'g5': (18, 5, 12), 'h5': (18, 2, 12),
    'a6': (21, 23, 12), 'b6': (21, 20, 12), 'c6': (21, 17, 12), 'd6': (21, 14, 12),
    'e6': (21, 11, 12), 'f6': (21, 8, 12), 'g6': (21, 5, 12), 'h6': (21, 2, 12),
    'a7': (24, 23, 12), 'b7': (24, 20, 12), 'c7': (24, 17, 12), 'd7': (24, 14, 12),
    'e7': (24, 11, 12), 'f7': (24, 8, 12), 'g7': (24, 5, 12), 'h7': (24, 2, 12),
    'a8': (27, 23, 12), 'b8': (27, 20, 12), 'c8': (27, 17, 12), 'd8': (27, 14, 12),
    'e8': (27, 11, 12), 'f8': (27, 8, 12), 'g8': (27, 5, 12), 'h8': (27, 2, 12), 'discard': (15, 30, 12)
}

def is_square_reachable(square, square_coordinates, robot):
    """
    Check if the target square is reachable using the robot's inverse kinematics.

    Parameters:
    square (str): Target square (e.g., 'e2').
    square_coordinates (dict): Mapping of squares to coordinates.
    robot (ChessRobotArm): The robotic arm instance.

    Returns:
    bool: True if the square is reachable, False otherwise.
    """
    if square not in square_coordinates:
        return False  # Square not found in the provided coordinates

    # Get the x, y, z coordinates for the square
    x, y, z = square_coordinates[square]

    try:
        # Run the inverse kinematics calculation
        theta1, theta2, theta3 = robot.calculate_inverse_kinematics(x, y, z, 12.1, 12.1)

        # Ensure the angles are valid floats and not zero
        if all(angle != 0 for angle in [theta1, theta2, theta3]):
            return True  # Valid theta values mean the square is reachable
    except ValueError:
        pass  # Ignore ValueError raised for out-of-reach positions

    return False  # Default to unreachable if an exception occurs or invalid angles

# Game loop
while not board.is_game_over():
    if board.turn == chess.BLACK:
        # Human's turn
        print("It's your turn (Black).")
        user_move = input("Make your move (e.g., e2e4): ")
        try:
            board.push_uci(user_move)  # Validate and apply the move
        except chess.IllegalMoveError:
            print(f"Illegal move: {user_move}. Please try again.")
            continue  # Prompt again for a valid move
    else:
        # Computer's turn
        print("Computer is thinking...")
        while True:
            result = engine.play(board, chess.engine.Limit(time=random.random()))
            comp_move = result.move.uci()
            (sq1, sq2) = (comp_move[:2], comp_move[2:4])  # Get source and target squares
            if is_square_reachable(sq1, square_coordinates, robot) and is_square_reachable(sq2, square_coordinates, robot):
                break  # Valid move found
            print(f"Move {comp_move} is out of reach. Generating a new move...")
        print(f"{sq1}, {sq2}")
            # Check for capturing a piece
        if board.is_capture(result.move):
            print(f"Computer captures a piece at {sq2}")
            #robot.move_to_square(sq2, square_coordinates)  # Move to captured square
            #robot.send_motor_times(0.5, 0.5, 0.5)  # Pick up captured piece
            #robot.rest()  # Return to rest position
            #robot.move_to_square('discard', square_coordinates)  # Move to discard location
            #robot.send_motor_times(0.5, 0.5, 0.5)  # Drop the captured piece
            #robot.rest()  # Return to rest position

            # Handle castling moves
        if comp_move == 'e1g1' and board.piece_type_at(chess.E1) == chess.KING:  # Kingside castling
            print("Computer castles kingside.")
            #robot.move_to_square('h1', square_coordinates)  # Move to rook's source square
            #robot.send_motor_times(0.5, 0.5, 0.5)  # Pick up the rook
            #robot.rest()  # Return to rest position
            #robot.move_to_square('f1', square_coordinates)  # Move to rook's target square
            #robot.send_motor_times(0.5, 0.5, 0.5)  # Place the rook
            #robot.rest()  # Return to rest position
        elif comp_move == 'e1c1' and board.piece_type_at(chess.E1) == chess.KING:  # Queenside castling
            print("Computer castles queenside.")
            #robot.move_to_square('a1', square_coordinates)  # Move to rook's source square
            #robot.send_motor_times(0.5, 0.5, 0.5)  # Pick up the rook
            #robot.rest()  # Return to rest position
            #robot.move_to_square('d1', square_coordinates)  # Move to rook's target square
            #robot.send_motor_times(0.5, 0.5, 0.5)  # Place the rook
            #robot.rest()  # Return to rest position

        # Execute the computer's move
        robot.move_to_square(sq1, square_coordinates, gripper_orientation="close")  # Move to source square
        #robot.send_motor_times(0.5, 0.5, 0.5)  # Pick up the piece
        #robot.rest()  # Return to rest position
        robot.move_to_square(sq2, square_coordinates, gripper_orientation="open")  # Move to target square
        #robot.send_motor_times(0.5, 0.5, 0.5)  # Place the piece
        #robot.rest()  # Return to rest position
        board.push(result.move)  # Push the move to the board

        # Display the computer's move
        print(f"Robot (Computer) plays: {comp_move}")

    # Display the updated board
    print(board)

# End of the game
if board.is_checkmate():
    print("Checkmate!")
elif board.is_stalemate():
    print("Stalemate!")
elif board.is_insufficient_material():
    print("Draw due to insufficient material.")
else:
    print("Game over!")

# Clean up the chess engine
engine.quit()
