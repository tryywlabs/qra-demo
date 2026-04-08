from pathlib import Path

from django.http import Http404
from django.shortcuts import render
from django.urls import reverse


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MODULES = {
    "leak": {
        "title": "Leak",
        "category": "Leak",
        "heading": "Leaks",
        "description": "Mass-release calculators for gas, liquid, and two-phase leak scenarios.",
        "directory": PROJECT_ROOT / "qra_scripts" / "leak",
        "href": "leak:dashboard",
        "kind": "app",
        "accent": "leak",
    },
    "gas_dispersion": {
        "title": "Gas Dispersion",
        "category": "Consequence",
        "heading": "Consequences",
        "description": "Atmospheric dispersion scripts for plume and puff release modelling.",
        "directory": PROJECT_ROOT / "qra_scripts" / "gas",
        "href": "gas_dispersion_dashboard",
        "kind": "app",
        "accent": "dispersion",
    },
    "fire": {
        "title": "Fire",
        "category": "Consequence",
        "heading": "Consequences",
        "description": "Thermal consequence calculator for pool-fire radiation scenarios.",
        "directory": PROJECT_ROOT / "qra_scripts" / "fire",
        "href": "fire_dashboard",
        "kind": "app",
        "accent": "fire",
    },
    "explosion": {
        "title": "Explosion",
        "category": "Consequence",
        "heading": "Consequences",
        "description": "Blast consequence calculators covering TNT, TNO, and BST workflows.",
        "directory": PROJECT_ROOT / "qra_scripts" / "explosion",
        "href": "explosion_dashboard",
        "kind": "app",
        "accent": "explosion",
    },
}


def _list_scripts(directory: Path) -> list[str]:
    if not directory.exists():
        return []
    return sorted(path.name for path in directory.glob("*.py"))


def home(request):
    sections = {
        "Leaks": [],
        "Consequences": [],
    }

    for module_key, module in MODULES.items():
        sections[module["heading"]].append(
            {
                "key": module_key,
                "title": module["title"],
                "description": module["description"],
                "accent": module["accent"],
                "script_count": len(_list_scripts(module["directory"])),
                "href": reverse(module["href"]),
                "kind": module["kind"],
            }
        )

    context = {
        "leak_modules": sections["Leaks"],
        "consequence_modules": sections["Consequences"],
    }
    return render(request, "landing.html", context)


def module_directory(request, module_key: str):
    module = MODULES.get(module_key)
    if module is None or module["kind"] != "directory":
        raise Http404("Module not found")

    scripts = _list_scripts(module["directory"])
    context = {
        "module": {
            "title": module["title"],
            "description": module["description"],
            "accent": module["accent"],
            "directory_name": module["directory"].name,
            "script_count": len(scripts),
        },
        "scripts": scripts,
    }
    return render(request, "module_directory.html", context)
