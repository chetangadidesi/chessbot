import math
import serial
from time import sleep

class ChessRobotArm:
    def __init__(self, port='COM5', baudrate=9600, verbose=False):
        """
        Initialize the robotic arm connection and set verbose mode.
        """
        self.ser = serial.Serial(port, baudrate, timeout=1)  # Connect to Arduino
        sleep(2)  # Allow time for connection to stabilize
        self.verbose = verbose
        print(f"Connected to Arduino on {port}")
    """    
    def send_motor_times(self, base_time, shoulder_time, elbow_time):
        
        #Send motor times (in milliseconds) to the Arduino via serial.
    
        command = f"{base_time:.2f},{shoulder_time:.2f},{elbow_time:.2f}\n"
        self.ser.write(command.encode())
        if self.verbose:
            print(f"Sent to Arduino: {command}")
        sleep(0.1)

    def send_gripper_orientation(self, gripper_orientation):
        
        #Send motor times (in milliseconds) to the Arduino via serial.
        
        command = f"{gripper_orientation}\n"
        self.ser.write(command.encode())
        if self.verbose:
            print(f"Sent to Arduino: {command}")
        sleep(0.1)
    """

    def send_data(self, base_time, shoulder_time, elbow_time, gripper_orientation):
        """
        Send motor times and gripper orientation to the Arduino via serial.
        """
        # Combine motor times and gripper orientation into one command string
        command = f"{base_time:.2f},{shoulder_time:.2f},{elbow_time:.2f},{gripper_orientation}\n"
        self.ser.write(command.encode())  # Send the command over serial.
    
        if self.verbose:
            print(f"Sent to Arduino: {command}")  # Print the sent data for debugging.
    
        sleep(0.1)  # Add a small delay to avoid overloading the serial communication.

    def calculate_motor_time(self, target_angle, current_angle, speed_deg_per_sec):
        """
        Calculate the time and direction needed for a motor to reach the target angle.
        """
        delta_angle = abs(target_angle - current_angle)
        time_needed = delta_angle / speed_deg_per_sec
        direction = "FORWARD" if target_angle > current_angle else "BACKWARD"
        return time_needed, direction

    def calculate_inverse_kinematics(self, x, y, z, r2, r3):
        """
        Calculate inverse kinematics for the OWI robotic arm.
        """
        
        theta1 = math.atan2(y, x)
        r_xy = math.sqrt(x**2 + y**2)
        D = (r_xy**2 + z**2 - r2**2 - r3**2) / (2 * r2 * r3)
        if abs(D) <= 1:
            theta3 = math.atan2(-math.sqrt(1 - D**2), D)  # Elbow up
            r23 = r2 + r3 * math.cos(theta3)
            theta2 = math.atan2(z, r_xy) - math.atan2(r3 * math.sin(theta3), r23)
            return math.degrees(theta1), math.degrees(theta2), math.degrees(theta3)
        else:
            theta1 = 0
            theta2 = 0
            theta3 = 0
            
            print("Target position out of reach.")
            return theta1, theta2, theta3

    def move_to_square(self, square, square_coordinates, gripper_orientation, speed=14):
        """
        Move the robotic arm to a specified chess square using inverse kinematics.

        Parameters:
        square (str): Target square (e.g., 'e2').
        square_coordinates (dict): Mapping of squares to coordinates.
        speed (float): Motor speed in degrees/sec.
        """
        if square not in square_coordinates:
            print(f"Invalid square: {square}")
            return False  # Signal failure

        x, y, z = square_coordinates[square]
        theta1, theta2, theta3 = self.calculate_inverse_kinematics(x, y, z, 12.1, 12.1)

        # Check if target position is out of reach or all thetas are zero
        if (theta1 == 0 and theta2 == 0 and theta3 == 0):
            print(f"Target position {square} out of reach. Please re-enter a valid square.")
            return False  # Exit the method immediately

        print(f"Moving to {square} with angles: {theta1:.2f}, {theta2:.2f}, {theta3:.2f}")

        # Assume initial angles are 0
        current_angles = [0, 60, -60]
        theta_target = [theta1, theta2, theta3]
        motor_times = []

        for current, target in zip(current_angles, theta_target):
            time, _ = self.calculate_motor_time(target, current, speed)
            motor_times.append(time * 1000)  # Convert to milliseconds


        # Send motor times to Arduino
        #self.send_motor_times(*motor_times)  
        #print(f"Motor times: {motor_times}")
        #self.send_gripper_orientation(gripper_orientation) 
        #print(f"Gripper Orientation: {gripper_orientation}")
        self.send_data(*motor_times, gripper_orientation)
        print(f"Motor Times: {motor_times}")
        print(f"Gripper Orientation: {gripper_orientation}")
        return True  # Signal success
    
    def rest(self):
        """
        Return the arm to the rest position.
        """
        #self.send_motor_times(0, 0, 0) 
        print("Arm returned to rest position.")

# Define chessboard coordinates
square_coordinates = {
    'a1': (6, 23, 12), 'b1': (6, 20, 12), 'c1': (6, 17, 12), 'd1': (6, 14, 12),
    'e1': (6, 11, 12), 'f1': (6, 8, 12), 'g1': (6, 5, 12), 'h1': (6, 2, 12),
    'a2': (9, 23, 12), 'b2': (9, 20, 12), 'c2': (9, 17, 12), 'd2': (9, 14, 12),
    'e2': (9, 11, 12), 'f2': (9, 8, 12), 'g2': (9, 5, 12), 'h2': (9, 2, 12),
    'a3': (12, 23, 12), 'b3': (12, 20, 12), 'c3': (12, 17, 8), 'd3': (12, 14, 12),
    'e3': (12, 11, 12), 'f3': (12, 8, 12), 'g3': (12, 5, 8), 'h3': (12, 2, 12),
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
if __name__ == "__main__":
    robot = ChessRobotArm(port='COM5', verbose=True)

    while True:
        while True:
            # Request both squares at the start
            square = input("Enter a square to pick up from (e.g., e2): ").strip()
            if square.lower() == "exit":
                robot.rest()
                exit()

            square2 = input("Enter a square to move to (e.g., e4): ").strip()
            if square2.lower() == "exit":
                robot.rest()
                exit()

            # Validate both squares
            x1, y1, z1 = square_coordinates.get(square, (None, None, None))
            x2, y2, z2 = square_coordinates.get(square2, (None, None, None))

            if None in (x1, y1, z1) or None in (x2, y2, z2):
                print("Invalid square(s). Please re-enter both squares.")
                continue

            theta1_pickup = robot.calculate_inverse_kinematics(x1, y1, z1, 12.1, 12.1)
            theta1_move = robot.calculate_inverse_kinematics(x2, y2, z2, 12.1, 12.1)

            if all(angle == 0 for angle in theta1_pickup) or all(angle == 0 for angle in theta1_move):
                print("One or both positions are out of reach. Please re-enter both squares.")
                continue  # Restart the loop for new inputs

            # If both squares are valid, move to the pickup square
            #print(f"Moving to {square} with angles: {theta1_pickup[0]:.2f}, {theta1_pickup[1]:.2f}, {theta1_pickup[2]:.2f}")
            robot.move_to_square(square, square_coordinates, gripper_orientation="close")

            # Move to the target square
            #print(f"Moving to {square2} with angles: {theta1_move[0]:.2f}, {theta1_move[1]:.2f}, {theta1_move[2]:.2f}")
            robot.move_to_square(square2, square_coordinates, gripper_orientation="open")
            
            # Exit the loop after successfully completing the task
            break




        #robot.rest()

