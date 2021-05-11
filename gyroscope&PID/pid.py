from simple_pid import PID
from mpu6050 import mpu6050
mpu= mpu6050(0x68)
mpu.set_accel_range(0x18)

pid=PID(00.1,0.1,0.05,setpoint=0)
pid.sample_time = 0.02
pid.output_limits =(0, 1.0)

accel_data=mpu.get_accel_data()
xacc=(accel_data['x'])
while True:
   accel_data=mpu.get_accel_data()
   xacc=(accel_data['x'])
   step=pid(xacc)
   print("step: " +str(step))
