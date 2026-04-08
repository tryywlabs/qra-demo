# 함수: Q_o 계산
def calculate_Qo(ratio_GOR, Q_g, Q_L):
    GOR = float(ratio_GOR)  # 가스 오일 비율
    Q_g = float(Q_g)   # 기체 방출률 (kg/s)
    Q_L = float(Q_L)   # 액체 방출률 (kg/s)
    
    # Qo = (GOR / (GOR + 1)) * Qg + (1 / (GOR + 1)) * QL
    res = (GOR / (GOR + 1)) * Q_g + (1 / (GOR + 1)) * Q_L

    return res