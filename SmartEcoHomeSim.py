# --- STATE VARIABLES ---
temperature = 25          # Current room temperature in °C
motion_detected = True     # Occupancy status (True = someone is in the room)
current_energy_used = 0   # Counter tracking cumulative energy consumption
energy_limit = 600         # Maximum threshold before system trip
is_power_saver = False     # Tracks if power saver mode is active


# --- FUNCTIONS ---

def check_hvac(temp):
    """Manages Heating, Ventilation, and Air Conditioning based on thresholds."""
    if temp > 23:
        return "AC is ON (Cooling)"
    elif temp < 18:
        return "Heater is ON (Heating)"
    else:
        return "HVAC is OFF (Eco Range)"

def check_lighting(motion, time_24h):
    """Handles smart lighting with nested logic for night dimming."""
    if motion:
        # Nested conditional: check time threshold if someone is in the room
        if time_24h >= 22 or time_24h < 6:
            return "Lights are ON (Dimmed to 20% for night)"
        else:
            return "Lights are ON (100% Brightness)"
    else:
        return "Lights are OFF (No motion)"
    
# --- MAIN SIMULATION LOOP ---
# The simulation runs as long as we haven't completely blacked out the grid
time_hour = 18  # Start simulation at 6:00 PM (18:00)

print("--- Starting Smart Eco-Home Simulation ---\n")

while current_energy_used < energy_limit:
    print(f"[Time: {time_hour}:00 | Energy Used: {current_energy_used} kWh / {energy_limit} kWh]")
    
    # 1. Evaluate Sub-programs
    hvac_status = check_hvac(temperature)
    lighting_status = check_lighting(motion_detected, time_hour)
    
    print(f"-> Room Status: {hvac_status}")
    print(f"-> Light Status: {lighting_status}")
    
    # 2. Accumulate Energy Based on Status
    if "AC" in hvac_status or "Heater" in hvac_status:
        current_energy_used += 40  # Climate control uses heavy energy
    if "100%" in lighting_status:
        current_energy_used += 10
    elif "Dimmed" in lighting_status:
        current_energy_used += 2   # Lower draw when dimmed
        
    # 3. Data Analysis: Nested loop for Warning Flash if usage gets high (> 80%)
    if current_energy_used > 400 and not is_power_saver:
        print("\n--- WARNING SYSTEM TRIGGERED ---")
        # Nested loop: Blink warning light exactly 3 times
        for blink in range(1, 4):
            print(f"⚠️ [Blink {blink}] Flash Warning: Energy Usage Exceeded 80% Threshold!")
        
        # Enforce Power Saver Mode to change code behavior dynamically
        print("-> Activating Power Saver Mode: Dimming systems...\n")
        is_power_saver = True
        motion_detected = False # Force lights off/occupants to leave to save energy
        temperature = 21        # Bring HVAC to a neutral rest state
        
    # Advance time simulation
    time_hour = (time_hour + 1) % 24
    print("-" * 50)

# --- LOOP EXIT (DATA THRESHOLD BREACHED) ---
print(f"\n🚨 [CRITICAL ALERT] Current energy ({current_energy_used} kWh) exceeded the limit ({energy_limit} kWh)!")
print("🚨 Main Power Breaker Tripped. Simulation Terminated Safely.")