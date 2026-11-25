"""Output folders for every generated file. One place to change the repo layout."""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DXF, DXF_FLAT, PREV, ANIM = ROOT / "dxf", ROOT / "dxf" / "backup_flat", ROOT / "previews", ROOT / "animation"

STEP_DIRS = {
    "assemblies": ROOT / "step" / "1_assemblies",
    "print": ROOT / "step" / "2_print",
    "laser_cut": ROOT / "step" / "3_laser_cut",
    "machined": ROOT / "step" / "4_machined",
    "bought": ROOT / "step" / "5_bought",
}
F360_DIRS = {
    "assemblies": ROOT / "fusion360_import" / "1_assemblies",
    "print": ROOT / "fusion360_import" / "2_print_parts",
    "sketches": ROOT / "fusion360_import" / "3_sketches",
}


def step(cat, name):
    d = STEP_DIRS[cat]
    d.mkdir(parents=True, exist_ok=True)
    return d / f"{name}.step"


def to_f360(src, cat, new_name=None):
    d = F360_DIRS[cat]
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(src, d / (new_name or Path(src).name))
