import time
from simple_pid import PID

co2_setpoint_from_app = 450 #fed from webapp API
co2_from_simulator = 400 #fed from simulator API
pid = PID(-5, -0.5, -10, setpoint=co2_setpoint_from_app) # set by an engineer
pid.output_limits = (0, 100) # minimum window is 0 max is 100
pid.sample_time = 5 # set by an engineer

current_co2 = 460 #current level of co2 in the room measured in ppm 
atmospheric_co2 = 400 #current level of co2 in the atmosphere measured in ppm
window_position = 0 #0 closed 100 fully open
update_period = 1 #in seconds, how frequently the co2 should update
people = 1 # amount of people in the room
last_time = time.time() #set the current time into variable


co2_increase_per_s = people*(1/10) #If window is fully closed then increase CO2 by 6 every 60 second per person
co2_decrease_per_s = -2 #If window is fully open then CO2 decreases by 2 every second



while True:
    if (time.time() - last_time) > update_period:
        current_co2 += (((1-(window_position/100))*co2_increase_per_s)+(window_position/100*co2_decrease_per_s))*update_period
        #^^ If window is partially open it is a weighted sum of increase and decrease
        if current_co2 < atmospheric_co2:
            current_co2 = atmospheric_co2
        print(current_co2)
        last_time = time.time()
        
    window_position = pid(current_co2)
    
    print("window position", window_position)
    time.sleep(1)
