################################################################################
# config.py
# Holds all configuration functions used in the main glider.py script.
#
# Author:  Kevin McAndrew
# Created: 27 October 2020
################################################################################

import os, ujson

def readConfig(pitch_pid, roll_pid, speed_pid):
    with open("/Web/www/pid.json", "r") as f:
        json_file = ujson.load(f)
        #global pitch_pid, roll_pid, speed_pid
        # Assign parameters
        # Pitch
        if pitch_pid.params["ki"] != float(json_file[0]["data"]["i"]):
            pitch_pid.integral = 0
            print("New config")
        pitch_pid.params["kp"] = float(json_file[0]["data"]["p"])
        pitch_pid.params["ki"] = float(json_file[0]["data"]["i"])
        pitch_pid.params["kd"] = float(json_file[0]["data"]["d"])
        # Roll
        if roll_pid.params["ki"] != float(json_file[1]["data"]["i"]):
            roll_pid.integral = 0
        roll_pid.params["kp"] = float(json_file[1]["data"]["p"])
        roll_pid.params["ki"] = float(json_file[1]["data"]["i"])
        roll_pid.params["kd"] = float(json_file[1]["data"]["d"])
        # Speed
        if speed_pid.params["ki"] != float(json_file[2]["data"]["i"]):
            speed_pid.integral = 0
        speed_pid.params["kp"] = float(json_file[2]["data"]["p"])
        speed_pid.params["ki"] = float(json_file[2]["data"]["i"])
        speed_pid.params["kd"] = float(json_file[2]["data"]["d"])
    with open("/Web/www/autre.json", "r") as f:
        json_file = ujson.load(f)
        # Assign parameters
        pitch_pid.initial = float(json_file[2]["data"]["target"])
        roll_pid.initial = float(json_file[1]["data"]["target"])
        speed_pid.initial= float(json_file[0]["data"]["target"])
    # Log file
    with open("/Web/www/log.json", "r") as f:
        log_file = ujson.load(f)
    '''with open("/Web/www/log.json", "w") as f:
        speed_read = speed.read()
        if speed_read != None and speed_read < 50:
            log_file[0]["data"] = speed_read
        ujson.dump(log_file, f)'''