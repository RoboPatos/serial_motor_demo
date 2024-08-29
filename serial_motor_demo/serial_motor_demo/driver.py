import rclpy
from rclpy.node import Node
from serial_motor_demo_msgs.msg import MotorCommand
import time
import math
import serial
from threading import Lock

class MotorDriver(Node):

    def __init__(self):
        super().__init__('motor_driver')


        # Setup parameters

        self.declare_parameter('serial_port', value="/dev/ttyUSB0")
        self.serial_port = self.get_parameter('serial_port').value


        self.declare_parameter('baud_rate', value=57600)
        self.baud_rate = self.get_parameter('baud_rate').value


        self.declare_parameter('serial_debug', value=False)
        self.debug_serial_cmds = self.get_parameter('serial_debug').value
        if (self.debug_serial_cmds):
            print("Serial debug enabled")


        # Setup topics & services

        self.subscription = self.create_subscription(
            MotorCommand,
            'motor_command',
            self.motor_command_callback,
            10)

        # Envia para GUI
        # self.speed_pub = self.create_publisher(MotorVels, 'motor_vels', 10)

        # self.encoder_pub = self.create_publisher(EncoderVals, 'encoder_vals', 10)
        

        # Member Variables

        self.last_enc_read_time = time.time()
        
        self.mutex = Lock()

        # Open serial comms

        print(f"Connecting to port {self.serial_port} at {self.baud_rate}.")
        self.conn = serial.Serial(self.serial_port, self.baud_rate, timeout=1.0)
        print(f"Connected to {self.conn}")
        

    # Raw serial commands
    
    def send_pwm_motor_command(self, mot_1_speed, mot_2_speed):
        print(f"o {int(mot_1_speed)} {int(mot_2_speed)}")
        self.send_command(f"o {int(mot_1_speed)} {int(mot_2_speed)}")
        # para testar com velocidade fixa
        # self.send_command(f"5") 

    # More user-friendly functions

    def motor_command_callback(self, motor_command):
        print('cmd recebido')
        self.send_pwm_motor_command(motor_command.mot_1_speed, motor_command.mot_2_speed)

    # Utility functions

    def send_command(self, cmd_string):
        
        self.mutex.acquire()
        try:
            cmd_string += "\r"
            self.conn.write(cmd_string.encode("utf-8"))
            if (self.debug_serial_cmds):
                print("Sent: " + cmd_string)

            ## Adapted from original
            c = ''
            value = ''
            while c != '\r':
                c = self.conn.read(1).decode("utf-8")
                if (c == ''):
                    print("Error: Serial timeout on command: " + cmd_string)
                    return ''
                value += c

            value = value.strip('\r')

            if (self.debug_serial_cmds):
                print("Received: " + value)
            return value
        finally:
            self.mutex.release()

    def close_conn(self):
        self.conn.close()



def main(args=None):
    
    rclpy.init(args=args)

    motor_driver = MotorDriver()

    rate = motor_driver.create_rate(2)
    while rclpy.ok():
        rclpy.spin_once(motor_driver)
        # motor_driver.check_encoders()


    motor_driver.close_conn()
    motor_driver.destroy_node()
    rclpy.shutdown()


