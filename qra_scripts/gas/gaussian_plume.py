import numpy as np

# -----------------------------
# Gaussian plume model functions
# -----------------------------
def sigma_yz(x, stability_class):
    """Compute dispersion coefficients σy and σz based on stability class (ALCHe/CCPS, 1996)"""
    if stability_class == 'A':
        sigma_y = 0.22 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.20 * x
    elif stability_class == 'B':
        sigma_y = 0.16 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.12 * x
    elif stability_class == 'C':
        sigma_y = 0.11 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.08 * x * (1 + 0.0002 * x) ** -0.5
    elif stability_class == 'D':
        sigma_y = 0.08 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.06 * x * (1 + 0.0015 * x) ** -0.5
    elif stability_class == 'E':
        sigma_y = 0.06 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.03 * x * (1 + 0.0003 * x) ** -1
    elif stability_class == 'F':
        sigma_y = 0.04 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.016 * x * (1 + 0.0003 * x) ** -1
    else:
        raise ValueError("Invalid stability class")
    return sigma_y, sigma_z


def gaussian_plume(Qevp, u_wind, H_E, x, y, z, stability_class):
    """Calculate Gaussian plume concentration C(x,y,z;H_E)"""
    sigma_y, sigma_z = sigma_yz(x, stability_class)
    term1 = Qevp / (2 * np.pi * u_wind * sigma_y * sigma_z)
    term2 = np.exp(-y**2 / (2 * sigma_y**2))
    term3 = np.exp(-((H_E - z)**2) / (2 * sigma_z**2))
    term4 = np.exp(-((H_E + z)**2) / (2 * sigma_z**2))
    C = term1 * term2 * (term3 + term4)
    return C, sigma_y, sigma_z