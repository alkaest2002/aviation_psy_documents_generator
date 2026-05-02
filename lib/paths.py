from pathlib import Path

def get_paths():
    base_path: Path = Path(__file__).resolve().parent.parent
    lib_path: Path = base_path / "lib"
    templates_path: Path = lib_path / "templates"
    data_path: Path = base_path / "../../sites/aviation-psy/src/program.json"
    output_path: Path = base_path / "out"

    return base_path, data_path, output_path, lib_path, templates_path