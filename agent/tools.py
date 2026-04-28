import pathlib
import subprocess
import shutil
from typing import Tuple, Optional

from langchain_core.tools import tool

# ---------------- PROJECT ROOT ----------------
PROJECT_ROOT = pathlib.Path.cwd() / "generated_project"


# ---------------- SAFE PATH HANDLER ----------------
def safe_path_for_project(path: str) -> pathlib.Path:
    """Ensures all file operations stay inside project directory."""
    p = (PROJECT_ROOT / path).resolve()

    if PROJECT_ROOT.resolve() not in p.parents and PROJECT_ROOT.resolve() != p.parent:
        raise ValueError("Attempt to write outside project root")

    return p


# ---------------- WRITE FILE (SAFE + BACKUP) ----------------
@tool
def write_file(path: str, content: str) -> str:
    """Writes content to a file inside the project directory with automatic backup."""

    p = safe_path_for_project(path)
    p.parent.mkdir(parents=True, exist_ok=True)

    # backup existing file
    if p.exists():
        backup_path = p.with_suffix(p.suffix + ".bak")
        shutil.copy(p, backup_path)

    # write new content
    with open(p, "w", encoding="utf-8") as f:
        f.write(content)

    return f"WROTE: {p}"


# ---------------- READ FILE ----------------
@tool
def read_file(path: str) -> str:
    """Reads and returns file content from the project directory."""

    p = safe_path_for_project(path)

    if not p.exists():
        return ""

    with open(p, "r", encoding="utf-8") as f:
        return f.read()


# ---------------- GET PROJECT DIRECTORY ----------------
@tool
def get_current_directory() -> str:
    """Returns the root directory of the generated project."""
    return str(PROJECT_ROOT)


# ---------------- LIST FILES ----------------
@tool
def list_files(directory: str = ".") -> str:
    """Lists all files inside the project directory recursively."""

    p = safe_path_for_project(directory)

    if not p.is_dir():
        return f"ERROR: {p} is not a directory"

    files = [
        str(f.relative_to(PROJECT_ROOT))
        for f in p.glob("**/*")
        if f.is_file()
    ]

    return "\n".join(files) if files else "No files found."


# ---------------- RUN SHELL COMMAND ----------------
@tool
def run_cmd(cmd: str, cwd: Optional[str] = None, timeout: int = 30) -> Tuple[int, str, str]:
    """Runs a shell command inside the project directory and returns output."""

    cwd_dir = safe_path_for_project(cwd) if cwd else PROJECT_ROOT

    result = subprocess.run(
        cmd,
        shell=True,
        cwd=str(cwd_dir),
        capture_output=True,
        text=True,
        timeout=timeout
    )

    return result.returncode, result.stdout, result.stderr


# ---------------- INIT PROJECT ----------------
def init_project_root() -> str:
    """Creates project root directory if it doesn't exist."""
    PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
    return str(PROJECT_ROOT)