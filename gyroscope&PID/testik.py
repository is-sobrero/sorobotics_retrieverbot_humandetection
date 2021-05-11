from ik import IKSolver
from servo_handler import ServoHandler
from leg import Leg
import math
import time
from mpu6050 import mpu6050

BACK_LEFT_ADDRESS = 0x2E
FRONT_LEFT_ADDRESS = 0x3A
BACK_RIGHT_ADDRESS = 0x22

servo = ServoHandler(0x40)
# definisci parametri delle gambe
leg_bl = Leg(
    base_address=0x2e,
    scale_factor=ServoHandler.TOWERPRO_SF,
    shoulder_offset=-10,
    offsets=[0,-10,-7],
    back_axis=True
)

leg_fl = Leg(
    base_address=0x3a,
    shoulder_offset=5
)

leg_br = Leg(
    base_address=0x22,
    scale_factor=ServoHandler.TOWERPRO_SF,
    right_axis=True,
    shoulder_offset=3,
    back_axis=True
)

leg_fr = Leg(
    base_address=0x16,
    right_axis=True,
    shoulder_offset=10,
    offsets=[0,0,5],
)
mpu=mpu6050(0x68)
mpu.set_accel_range(0x18)

#range tolleranza giroscopio
range=0.5
nrange= -0.5
#step di movimento robot
step=0.05
#altezza robot
h = 15
hbl=h
hbr=h
hfr=h
hfl=h
ik = IKSolver(servo)
#inizializza robot
ik.solve(leg_bl, 0,5.5, h)
ik.solve(leg_fl,0,5.5, h)
ik.solve(leg_br, 0, -5.5, h)
ik.solve(leg_fr, 0,-5.5,h)
time.sleep(2)
#inizializzare le variabili di posizione
accel_data=mpu.get_accel_data()
xac0=(accel_data['x'])
yac0=(accel_data['y'])
xacc2=xac0
yacc2=yac0

hbl=h
hfl=h
hbr=h
hfr=h

while True: #ciclo bilanciamento
    accel_data=mpu.get_accel_data()
    xacc=(accel_data['x']-xac0)
    yacc=(accel_data['y']-yac0)
    print("acc x : "+str(xacc))
    print()
    print("acc y : "+str(yacc))
    print()

    while xacc>range or xacc<-range or yacc>range or yacc<-range:  #equilibratore del robot
       if yacc>range:
          hbl= hbl - step
          hfl= hfl - step
          hbr= hbr + step
          hfr= hfr + step
       elif yacc<nrange:
          hbl = hbl + step
          hfl = hfl + step
          hbr = hbr - step
          hfr = hfr - step
       if  xacc>range:
          hbl= hbl + step
          hbr= hbr + step
          hfl= hfl - step
          hfr= hfr - step
       elif xacc<nrange:
          hbl = hbl - step
          hbr = hbr - step
          hfl = hfl + step
          hfr = hfr + step
      # while hbl<7 or hfl< 7 or hbr<7 or hfr<7:
       if hbl<7:
          hbl=7.5
       elif hbl>24:
          hbl=24.0
       if hfl<7:
          hfl=7.5
       elif hfl>24:
          hfl=24.0
       if hbr<7:
          hbr=7.5
       elif hbr>24:
          hbr=24
       if hfr<7:
          hfr=7.5
       elif hfr>24:
          hfr=24
       ik.solve(leg_bl, 0, 5.5, hbl)
       ik.solve(leg_fl, 0, 5.5, hfl)
       ik.solve(leg_br, 0, -5.5, hbr)
       ik.solve(leg_fr, 0, -5.5, hfr)
       accel_data=mpu.get_accel_data()
       xacc = (accel_data['x'] - xac0)
       yacc = (accel_data['y'] - yac0)
       print("acc x : "+str(xacc))
       print()
       print("acc y : "+str(yacc))
       print()
       print("hbl :" + str(hbl))
       print("hfl :" + str(hfl))
       print("hbr :" + str(hbr))
       print("hfr :" + str(hfr))
       print()


