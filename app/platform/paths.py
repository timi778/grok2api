"""Shared runtime paths derived from environment variables."""

import os
from pathlib import Path


_ROOT_DIR = Path(__file__).resolve().parents[2]


def _resolve_env_path(name: str, default: str) -> Path:
    raw = os.getenv(name, default).strip() or default
    path = Path(raw)
    if not path.is_absolute():
        path = _ROOT_DIR / path
    return path


def _resolve_writable_dir(name: str, default: str) -> Path:
    path = _resolve_env_path(name, default)
    try:
        path.mkdir(parents=True, exist_ok=True)
        return path
    except OSError:
        fallback = Path(os.getenv("TMPDIR", "/tmp")) / default
        fallback.mkdir(parents=True, exist_ok=True)
        return fallback


def data_dir() -> Path:
    return _resolve_writable_dir("DATA_DIR", "data")


def log_dir() -> Path:
    return _resolve_writable_dir("LOG_DIR", "logs")


def data_path(*parts: str) -> Path:
    return data_dir().joinpath(*parts)


def log_path(*parts: str) -> Path:
    return log_dir().joinpath(*parts)


__all__ = ["data_dir", "log_dir", "data_path", "log_path"]
