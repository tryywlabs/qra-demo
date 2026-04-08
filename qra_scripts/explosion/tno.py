def energy_context_calc(mass_part, lhv):
    energy = mass_part * lhv
    return energy

def scaled_distance_calc(distance, energy, p0):
    R = distance / (energy / p0 / 1000) ** (1/3) #/1000 for kj to mj conversion
    return R

def pressure_calc(R):
    p_s = 0.406 * (R ** -1.2)
    return p_s

def scenario_calc(energy, p0):
    res = []
    for scenario in range(1, 200):
        R = scaled_distance_calc(scenario, energy, p0)
        p_s = pressure_calc(R)
        res.append((scenario, R, p_s))
    return res
        #print(f"Distance: {scenario} m, Scaled Distance: {R:.2f}, Overpressure: {p_s:.4f} bar")