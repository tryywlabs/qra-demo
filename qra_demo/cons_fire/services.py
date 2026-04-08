from functools import lru_cache
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[2]
SCRIPT_ROOT = PROJECT_ROOT / "qra_scripts" / "fire"


def _load_module(module_name: str, module_path: Path):
    spec = spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load script module from {module_path}")

    module = module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@lru_cache(maxsize=1)
def _module():
    return _load_module("qra_scripts.fire.pool_fire", SCRIPT_ROOT / "pool_fire.py")


def calculate_pool_fire_model(**inputs):
    module = _module()
    fuel = inputs.pop("fuel")
    model_inputs = module.inputs_for_fuel(fuel, **inputs)
    result = module.calculate_pool_fire(model_inputs).to_dict()

    return {
        "radiation_flux": float(result["step6"]["Qrad"]),
        "flame_length": float(result["step1"]["LF"]),
        "smoke_yield": float(result["step2"]["Y"]),
        "soot_concentration": float(result["step3"]["Cs"]),
        "characteristic_length": float(result["step4"]["Lc"]),
        "mean_emissive_power": float(result["step5"]["E_bar"]),
        "view_factor": float(result["step6"]["Fv"]),
        "tau_atm": float(result["step6"]["tau_atm"]),
        "fuel": fuel,
        "fv_note": result["step6"]["fv_params"]["note"],
    }
