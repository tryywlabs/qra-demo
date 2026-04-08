import math

# --------------------------
# Briggs (1973) σy, σz 계수
# --------------------------
coeffs_briggs = {
    "A": (0.18, 0.92, 0.60, 0.75),
    "B": (0.14, 0.92, 0.53, 0.73),
    "C": (0.10, 0.92, 0.34, 0.71),
    "D": (0.06, 0.92, 0.15, 0.70),
    "E": (0.04, 0.92, 0.10, 0.65),
    "F": (0.02, 0.89, 0.05, 0.61),
}

# --------------------------
# Gaussian Puff 농도 계산 함수
# --------------------------
def calculate_concentration(mass, height, x, y, z, stability_class):
    Q = float(mass)     # total released mass (kg)
    H = float(height)   # effective height (m)
    x = float(x)        # downwind distance (m)
    y = float(y)        # crosswind distance (m)
    z = float(z)        # vertical position (m)
    stability = stability_class.strip()

    if stability not in coeffs_briggs:
        raise ValueError("Invalid stability class. Choose from A, B, C, D, E, F.")

    # Briggs 계수 선택
    a, b, c, d = coeffs_briggs[stability]

    # 분산계수 계산
    sigma_y = a * (x ** b)
    sigma_z = c * (x ** d)

    # Gaussian Puff 농도 계산식
    C = (Q / ((2 * math.pi) ** 1.5 * sigma_y * sigma_y * sigma_z)) * \
        math.exp(-0.5 * (y / sigma_y) ** 2) * \
        (math.exp(-0.5 * ((z - H) / sigma_z) ** 2) + math.exp(-0.5 * ((z + H) / sigma_z) ** 2))
    
    return C, sigma_y, sigma_z
