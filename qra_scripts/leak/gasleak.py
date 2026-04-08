import math

# 함수: Qg 계산
def calculate_Qg(diameter_mm, density_kg_m3, pressure_bar_gauge):
    d = float(diameter_mm)  # 구멍 직경 (mm)
    rho_g = float(density_kg_m3)  # 초기 가스 밀도 (kg/m^3)
    P_g_Pa = float(pressure_bar_gauge)  # 초기 가스 압력 (bar gauge)

    # 수식 적용: Qg = 1.4 * 10^-4 * d^2 * sqrt(rho_g * P_g)
    res = 1.4 * 10**-4 * d**2 * math.sqrt(rho_g * P_g_Pa)

    return res
