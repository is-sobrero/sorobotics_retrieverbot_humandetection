# Copyright 2021 I.S. "A. Sobrero" - SoRobotics Team. All rights reserved.
# Use of this source code is governed by the GPL 3.0 license that can be
# found in the LICENSE file.

import math
from leg import Leg
from servo_handler import ServoHandler

class ServoDomainError(Exception, Leg):
    pass

class IKSolver:
    #STD_THIGH_LEN = 12
    #STD_SHIN_LEN = 14
    STD_THIGH_LEN=10
    STD_SHIN_LEN =13
    HIP_OFFSET = 5.5

    def __init__(self, servo_handler=ServoHandler(0x40), use_interpolator=False, simulated_environment=False):
        if not type(servo_handler) is ServoHandler and not simulated_environment:
            raise Exception("Type of servo_handler must be ServoHandler")
        
        if not simulated_environment:
            self.servo_handler = servo_handler
        self.use_interpolator = use_interpolator
        self.simulated_environment = simulated_environment

    def solve(self, leg, x, y, z, output_deg=False):
        if not type(leg) is Leg:
            raise TypeError("Type of leg must be Leg")   
        # P(x,y,z) O(0,0,0)
        # length from O to P projection on YZ plane


        
        #DEVI CAMBIARE QUESTOOOOOOOO

        h=math.sqrt(x**2+y**2+z**2)

        
        # total height of the leg on th YZ plane
        dyz=math.sqrt(y**2+z**2)
        g=math.acos(-z/dyz)
        gamma = -g if leg.right_axis else g

        beta_offset = math.atan(x/h)
        new_z = h/math.cos(beta_offset)
        
        #utilizzo teorema del coseno
        beta_cos = (self.STD_THIGH_LEN**2 + new_z**2 - self.STD_SHIN_LEN**2 ) / (2*self.STD_THIGH_LEN*new_z)
        beta = math.acos(beta_cos) + math.pi/2 + beta_offset

        alpha_cos = (self.STD_THIGH_LEN**2 + self.STD_SHIN_LEN**2 - new_z**2) / (2*self.STD_THIGH_LEN*self.STD_SHIN_LEN)
        alpha = math.acos(alpha_cos)
        
        #conversion rad to deg
        alpha_deg = alpha * 180 / math.pi
        beta_deg = beta * 180 / math.pi
        gamma_deg = gamma * 180 / math.pi

        if self.simulated_environment:
            if output_deg:
                return alpha_deg, beta_deg, gamma_deg
            else:
                return alpha, beta, gamma

        final_alfa = leg.alfa_offset + (alpha_deg if not leg.right_axis else 180 - alpha_deg)
        final_beta = leg.beta_offset + (beta_deg if not leg.right_axis else 180 - beta_deg)
        final_gamma = leg.gamma_offset + (gamma_deg if not leg.invert_shoulder else 180 - gamma_deg)

        if final_alfa < 0:
            raise ServoDomainError("Alpha angle of leg is not positive", leg)   
        if final_beta < 0:
            raise ServoDomainError("Beta angle of leg is not positive", leg)   
        if final_gamma < 0:
            raise ServoDomainError("Gamma angle of leg is not positive", leg)   

        if not self.simulated_environment:
            self.servo_handler.write_channel(leg.base_address, final_gamma, leg.scale_factor)
            self.servo_handler.write_channel(leg.base_address + 4, final_beta, leg.scale_factor)
            self.servo_handler.write_channel(leg.base_address + 8, final_alfa, leg.scale_factor)
