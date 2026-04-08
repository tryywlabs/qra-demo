import math

def calculate_QL(diameter_mm, density_kg_m3, pressure_bar_gauge):
    d = float(diameter_mm)  # 구멍 직경 (mm)
    rho_L = float(density_kg_m3)  # 액체 밀도 (kg/m³)
    P_L_Pa = float(pressure_bar_gauge)  # 초기 압력 (bar gauge)

    # 수식 적용: QL = 2.1 * 10^-4 * d^2 * sqrt(rho_L * P_L)
    res = 2.1 * 10**-4 * d**2 * math.sqrt(rho_L * P_L_Pa)

    return res