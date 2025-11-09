import os
import shutil
import subprocess
from pathlib import Path


def _derive_repo_name(git_url: str) -> str:
    tail = (git_url or "").rstrip("/").split("/")[-1]
    if tail.endswith(".git"):
        tail = tail[:-4]
    return tail or "repo"

def _ensure_repo(git_url: str, base_root: str = "cloned_repositories") -> str:
    repo_name = _derive_repo_name(git_url)
    base_dir = os.path.join(base_root, repo_name)
    repo_dir = os.path.join(base_dir, "repo")

    os.makedirs(base_dir, exist_ok=True)

    git_dir = os.path.join(repo_dir, ".git")
    if os.path.isdir(git_dir):
        subprocess.run(["git", "-C", repo_dir, "fetch", "--all", "--prune"], check=False)
        return os.path.abspath(repo_dir)

    # Fresh clone
    if os.path.isdir(repo_dir):
        shutil.rmtree(repo_dir, ignore_errors=True)
    subprocess.run(["git", "clone", git_url, repo_dir], check=True)
    return os.path.abspath(repo_dir)

def _checkout(repo_dir: str, commit: str) -> None:
    subprocess.run(["git", "-C", repo_dir, "checkout", "-f", commit], check=True)

def _read_text_with_fallback(path: str) -> str:
    with open(path, "rb") as f:
        data = f.read()
    for enc in ("utf-8", "cp1252", "latin-1"):
        try:
            return data.decode(enc)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="ignore")

def _safe_repo_path(repo_dir: str, incoming_path: str) -> Path:
    repo_dir_abs = Path(repo_dir).resolve()
    p = Path(incoming_path)
    if not p.is_absolute():
        candidate = (repo_dir_abs / p).resolve()
    else:
        # If XML provides an absolute path, try to map it into repo_dir if it's already inside
        candidate = Path(incoming_path).resolve()
        # If it's not under repo_dir, try to make it relative to the repo root name tail
        try:
            # Prefer keeping as-is if it's already inside repo_dir
            candidate.relative_to(repo_dir_abs)
        except Exception:
            # Fallback: try to strip until the last "repo" segment
            parts = list(candidate.parts)
            if "repo" in parts:
                idx = parts.index("repo")
                candidate = (repo_dir_abs / Path(*parts[idx+1:])).resolve()

    # Final safety: must be inside repo_dir
    candidate.relative_to(repo_dir_abs)
    return candidate

def _slice_lines(text: str, startline: int, endline: int) -> str:
    if startline is None or endline is None or startline < 1 or endline < startline:
        return ""
    lines = text.splitlines(True)  # keep line endings
    start_idx = startline - 1
    end_idx = min(endline, len(lines))
    return "".join(lines[start_idx:end_idx])