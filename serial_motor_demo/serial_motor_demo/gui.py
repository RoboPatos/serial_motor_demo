import rclpy
from rclpy.node import Node
import time
from tkinter import *
import math

from serial_motor_demo_msgs.msg import MotorCommand

class MotorGui(Node):

    def __init__(self):
        super().__init__('motor_gui')

        self.publisher = self.create_publisher(MotorCommand, 'motor_command', 10)

        # Para receber info do driver/Arduino
        # self.speed_sub = self.create_subscription(
        #     MotorVels,
        #     'motor_vels',
        #     self.motor_vel_callback,
        #     10)

        # self.encoder_sub = self.create_subscription(
        #     EncoderVals,
        #     'encoder_vals',
        #     self.encoder_val_callback,
        #     10)

        self.tk = Tk()
        self.tk.title("SciCoBot")
        root = Frame(self.tk)
        root.pack(fill=BOTH, expand=True)

        
        Label(root, text="Controle individual dos motores").pack()


        m1_frame = Frame(root)
        m1_frame.pack(fill=X)
        Label(m1_frame, text="Motor 1").pack(side=LEFT)
        self.m1 = Scale(m1_frame, from_=-255, to=255, resolution=1, orient=HORIZONTAL)
        self.m1.pack(side=LEFT, fill=X, expand=True)

        m2_frame = Frame(root)
        m2_frame.pack(fill=X)
        Label(m2_frame, text="Motor 2").pack(side=LEFT)
        self.m2 = Scale(m2_frame, from_=-255, to=255, resolution=1, orient=HORIZONTAL)
        self.m2.pack(side=LEFT, fill=X, expand=True)

        motor_btns_frame = Frame(root)
        motor_btns_frame.pack()
        Button(motor_btns_frame, text='ENVIAR', command=self.send_motor_once).pack(side=LEFT)
        Button(motor_btns_frame, text='DINÂMICO.', command=self.show_values).pack(side=LEFT)
        Button(motor_btns_frame, text='PARAR DINÂMICO', command=self.show_values).pack(side=LEFT)
        Button(motor_btns_frame, text='PARAR', command=self.stop_motors).pack(side=LEFT)
        

    def show_values(self):
        print (self.m1.get(), self.m2.get())

    def send_motor_once(self):
        msg = MotorCommand()
        msg.mot_1_speed = float(self.m1.get())
        msg.mot_2_speed = float(self.m2.get())
        self.publisher.publish(msg)

    def stop_motors(self):
        msg = MotorCommand()
        msg.mot_1_speed = 0.0
        msg.mot_2_speed = 0.0
        self.publisher.publish(msg)

    def update(self):
        self.tk.update()

def main(args=None):
    
    rclpy.init(args=args)

    motor_gui = MotorGui()

    rate = motor_gui.create_rate(20)    
    while rclpy.ok():
        rclpy.spin_once(motor_gui)
        motor_gui.update()


    motor_gui.destroy_node()
    rclpy.shutdown()
