from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_ROOT = PROJECT_ROOT / "qra_scripts" / "leak"


def _load_module(module_name: str, file_name: str):
    module_path = SCRIPT_ROOT / file_name
    spec = spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load script module from {module_path}")

    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _modules():
    return {
        "gas": _load_module("qra_scripts.leak.gasleak", "gasleak.py"),
        "liquid": _load_module("qra_scripts.leak.liquidleak", "liquidleak.py"),
        "twophase": _load_module("qra_scripts.leak.twophaseleak", "twophaseleak.py"),
    }


def calculate_gas_leak(diameter_mm: float, density_kg_m3: float, pressure_bar_gauge: float) -> float:
    return _modules()["gas"].calculate_Qg(diameter_mm, density_kg_m3, pressure_bar_gauge)


def calculate_liquid_leak(
    diameter_mm: float,
    density_kg_m3: float,
    pressure_bar_gauge: float,
) -> float:
    return _modules()["liquid"].calculate_QL(diameter_mm, density_kg_m3, pressure_bar_gauge)


def calculate_two_phase_leak(ratio_GOR: float, Q_g: float, Q_L: float) -> float:
    return _modules()["twophase"].calculate_Qo(ratio_GOR, Q_g, Q_L)
