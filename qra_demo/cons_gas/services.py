import math
from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
GAS_SCRIPT_ROOT = PROJECT_ROOT / "qra_scripts" / "gas"


def _load_module(module_name: str, module_path: Path):
    spec = spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load script module from {module_path}")

    module = module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
    except ModuleNotFoundError as exc:
        if exc.name == "numpy":
            return None
        raise
    return module


@lru_cache(maxsize=1)
def _gas_modules():
    return {
        "plume": _load_module("qra_scripts.gas.gaussian_plume", GAS_SCRIPT_ROOT / "gaussian_plume.py"),
        "puff": _load_module("qra_scripts.gas.gaussian_puff", GAS_SCRIPT_ROOT / "gaussian_puff.py"),
    }


def _sigma_yz(x: float, stability_class: str):
    if stability_class == "A":
        sigma_y = 0.22 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.20 * x
    elif stability_class == "B":
        sigma_y = 0.16 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.12 * x
    elif stability_class == "C":
        sigma_y = 0.11 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.08 * x * (1 + 0.0002 * x) ** -0.5
    elif stability_class == "D":
        sigma_y = 0.08 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.06 * x * (1 + 0.0015 * x) ** -0.5
    elif stability_class == "E":
        sigma_y = 0.06 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.03 * x * (1 + 0.0003 * x) ** -1
    elif stability_class == "F":
        sigma_y = 0.04 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.016 * x * (1 + 0.0003 * x) ** -1
    else:
        raise ValueError("Invalid stability class")
    return sigma_y, sigma_z


def calculate_gaussian_plume(
    release_rate_kg_s: float,
    wind_speed_m_s: float,
    release_height_m: float,
    downwind_distance_m: float,
    crosswind_distance_m: float,
    receptor_height_m: float,
    stability_class: str,
):
    module = _gas_modules()["plume"]
    if module is not None:
        concentration, sigma_y, sigma_z = module.gaussian_plume(
            release_rate_kg_s,
            wind_speed_m_s,
            release_height_m,
            downwind_distance_m,
            crosswind_distance_m,
            receptor_height_m,
            stability_class,
        )
    else:
        sigma_y, sigma_z = _sigma_yz(downwind_distance_m, stability_class)
        term1 = release_rate_kg_s / (2 * math.pi * wind_speed_m_s * sigma_y * sigma_z)
        term2 = math.exp(-(crosswind_distance_m**2) / (2 * sigma_y**2))
        term3 = math.exp(-((release_height_m - receptor_height_m) ** 2) / (2 * sigma_z**2))
        term4 = math.exp(-((release_height_m + receptor_height_m) ** 2) / (2 * sigma_z**2))
        concentration = term1 * term2 * (term3 + term4)

    return {
        "concentration": float(concentration),
        "sigma_y": float(sigma_y),
        "sigma_z": float(sigma_z),
    }


def calculate_gaussian_puff(
    released_mass_kg: float,
    release_height_m: float,
    downwind_distance_m: float,
    crosswind_distance_m: float,
    receptor_height_m: float,
    stability_class: str,
):
    module = _gas_modules()["puff"]
    concentration, sigma_y, sigma_z = module.calculate_concentration(
        released_mass_kg,
        release_height_m,
        downwind_distance_m,
        crosswind_distance_m,
        receptor_height_m,
        stability_class,
    )
    return {
        "concentration": float(concentration),
        "sigma_y": float(sigma_y),
        "sigma_z": float(sigma_z),
    }
