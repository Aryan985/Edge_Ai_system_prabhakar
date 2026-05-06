# fusion/logic.py

from config import DISTANCE_THRESHOLD

def check_hazard(ai_detected, distance, ir_detected):
    
    if ai_detected and distance < DISTANCE_THRESHOLD:
        return True

    if ir_detected:
        return True
    
    if ai_detected and distance < 150:
        return True

    return False