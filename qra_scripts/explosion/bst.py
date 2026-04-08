def scaled_distance_calc(energy, p0, distance):
  R = distance / (energy / p0 / 1000) ** (1/3) #/1000 for kj to mj conversion
  return R

def pressure_calc(R):
  p_s = 0.085 * (R ** -1.05)
  return p_s

def scenario_calc(energy, p0):
  if energy <= 0 or p0 <= 0:
    raise ValueError("Energy and ambient pressure must be positive.")

  res = []
  for scenario in range(1, 200):
    R = scaled_distance_calc(energy, p0, scenario)
    p_s = pressure_calc(R)
    res.append((scenario, R, p_s))
  return res
