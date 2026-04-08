from dataclasses import dataclass

# Global variable to store TNT equivalent mass (W)
tnt_mass_global = None

# eta_values = {
#     lpg_lng = 0.02; #0.01 - 0.03, low efficiency
#     h2 = 0.06; #0.02 - 0.1, 0.1 is for congested areas
#     nh3 = 0.0125; #0.005 - 0.02 
# }

def calculate_tnt_equivalency(eta, mass, heat_combustion, tnt_heat_combustion, tnt_result):
    global tnt_mass_global
    try:
        # Get user input values for TNT equivalency
        eta = float(eta)
        mass = float(mass)
        heat_combustion = float(heat_combustion)
        tnt_heat_combustion = float(tnt_heat_combustion)

        # Calculate W using the formula
        tnt_mass_global = (eta * mass * heat_combustion) / tnt_heat_combustion
        #tnt heat of combustion is 4437 - 4765 kJ/kg. Use Metric. ASSUME 4680 kj/kg

        # Display the TNT equivalent mass result
        tnt_result = tnt_mass_global
        #round(tnt_result, 2)
        return tnt_result
    except ValueError:
        raise ValueError(f"Please enter valid numeric values for all fields.")
    
def scale_param_calc(mass_global, distance) -> float:
    z_e = distance / (mass_global ** (1/3))
    return z_e

def distance_pressure_calc(z_e) -> float:
    p_s = (573 * z_e ** -1.685) / 100
    return p_s

def per_distance_pressure(tnt_mass=None, start=1, end=200):
    mass = tnt_mass if tnt_mass is not None else tnt_mass_global
    if mass is None:
        raise ValueError("Please calculate TNT equivalent mass first.")
    start = int(start)
    end = int(end)
    if start <= 0 or end <= 0 or end < start:
        raise ValueError("Distance range must be positive and end >= start.")
    pressure_values = []
    for distance in range(start, end + 1):
        z_e = scale_param_calc(mass, distance)
        p_s = distance_pressure_calc(z_e)
        pressure_values.append((distance, p_s))
    return pressure_values
