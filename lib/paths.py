from pathlib import Path

class PathsError(Exception):
    """Custom exception for path-related errors."""
    pass

def get_paths():
    base_path: Path = Path(__file__).resolve().parent.parent
    lib_path: Path = base_path / "lib"
    templates_path: Path = lib_path / "templates"
    data_path: Path = base_path / "../../sites/aviation-psy/src/program.json"
    output_path: Path = base_path / "out"

    # check that all paths exist with some()
    if not all(p.exists() for p in [base_path, lib_path, templates_path, data_path, output_path]):
        missing = [str(p) for p in [base_path, lib_path, templates_path, data_path, output_path] if not p.exists()]
        raise PathsError(f"Missing required paths: {', '.join(missing)}")
    
    return base_path, data_path, output_path, lib_path, templates_path