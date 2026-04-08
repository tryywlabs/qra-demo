from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
EXPLOSION_SCRIPT_ROOT = PROJECT_ROOT / "qra_scripts" / "explosion"


def _load_module(module_name: str, module_path: Path):
    spec = spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load script module from {module_path}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _explosion_modules():
    return {
        "tnt": _load_module("qra_scripts.explosion.tnt", EXPLOSION_SCRIPT_ROOT / "tnt.py"),
        "tno": _load_module("qra_scripts.explosion.tno", EXPLOSION_SCRIPT_ROOT / "tno.py"),
        "bst": _load_module("qra_scripts.explosion.bst", EXPLOSION_SCRIPT_ROOT / "bst.py"),
    }


def calculate_tnt_equivalency(
    efficiency: float,
    mass_kg: float,
    heat_combustion_kj_kg: float,
    tnt_heat_combustion_kj_kg: float,
    distance_m: float,
):
    module = _explosion_modules()["tnt"]
    tnt_equivalent_mass = module.calculate_tnt_equivalency(
        efficiency,
        mass_kg,
        heat_combustion_kj_kg,
        tnt_heat_combustion_kj_kg,
        None,
    )
    scaled_distance = module.scale_param_calc(tnt_equivalent_mass, distance_m)
    peak_overpressure = module.distance_pressure_calc(scaled_distance)
    profile = [
        {"distance_m": distance, "peak_overpressure_bar": pressure}
        for distance, pressure in module.per_distance_pressure(tnt_equivalent_mass, 1, 50)
    ]
    return {
        "tnt_equivalent_mass": float(tnt_equivalent_mass),
        "scaled_distance": float(scaled_distance),
        "peak_overpressure": float(peak_overpressure),
        "profile": profile,
    }


def calculate_tno_overpressure(
    mass_participating_kg: float,
    lower_heating_value_kj_kg: float,
    ambient_pressure_pa: float,
    distance_m: float,
):
    module = _explosion_modules()["tno"]
    energy_kj = module.energy_context_calc(mass_participating_kg, lower_heating_value_kj_kg)
    scaled_distance = module.scaled_distance_calc(distance_m, energy_kj, ambient_pressure_pa)
    peak_overpressure = module.pressure_calc(scaled_distance)
    profile = [
        {
            "distance_m": distance,
            "scaled_distance": scaled,
            "peak_overpressure_bar": pressure,
        }
        for distance, scaled, pressure in module.scenario_calc(energy_kj, ambient_pressure_pa)[:50]
    ]
    return {
        "energy_kj": float(energy_kj),
        "scaled_distance": float(scaled_distance),
        "peak_overpressure": float(peak_overpressure),
        "profile": profile,
    }


def calculate_bst_overpressure(
    energy_kj: float,
    ambient_pressure_pa: float,
    distance_m: float,
):
    module = _explosion_modules()["bst"]
    scaled_distance = module.scaled_distance_calc(energy_kj, ambient_pressure_pa, distance_m)
    peak_overpressure = module.pressure_calc(scaled_distance)
    profile = [
        {
            "distance_m": distance,
            "scaled_distance": scaled,
            "peak_overpressure_bar": pressure,
        }
        for distance, scaled, pressure in module.scenario_calc(energy_kj, ambient_pressure_pa)[:50]
    ]
    return {
        "energy_kj": float(energy_kj),
        "scaled_distance": float(scaled_distance),
        "peak_overpressure": float(peak_overpressure),
        "profile": profile,
    }
