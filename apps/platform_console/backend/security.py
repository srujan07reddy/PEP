"""Shared security controls for the platform console API."""

import os
import re
from pathlib import Path
from typing import Iterable

from fastapi import HTTPException, UploadFile

MAX_UPLOAD_BYTES = int(os.getenv("PEP_MAX_UPLOAD_BYTES", str(10 * 1024 * 1024)))
SAFE_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,79}$")
SAFE_SLUG = re.compile(r"[^a-z0-9_-]+")


def safe_identifier(value: str, field_name: str) -> str:
    """Validate values that are later used to construct filesystem paths."""
    if not value or not SAFE_ID.fullmatch(value):
        raise HTTPException(status_code=400, detail=f"Invalid {field_name}")
    return value


def make_slug(value: str) -> str:
    slug = SAFE_SLUG.sub("_", value.strip().lower()).strip("_-")
    if not slug or len(slug) > 80 or not SAFE_ID.fullmatch(slug):
        raise HTTPException(status_code=400, detail="Invalid project name")
    return slug


def resolve_workspace_file(raw_path: str, workspace_root: Path) -> Path:
    """Resolve a readable file only inside the workspace or configured input roots."""
    candidate = Path(raw_path).expanduser().resolve()
    allowed_roots = [workspace_root.resolve()]
    configured = os.getenv("PEP_ALLOWED_INPUT_ROOTS", "")
    allowed_roots.extend(Path(item).expanduser().resolve() for item in configured.split(os.pathsep) if item)

    if not any(candidate == root or root in candidate.parents for root in allowed_roots):
        raise HTTPException(status_code=400, detail="Input path is outside an allowed workspace")
    if not candidate.is_file():
        raise HTTPException(status_code=400, detail="Input file does not exist")
    return candidate


async def read_upload(upload: UploadFile, allowed_extensions: Iterable[str]) -> bytes:
    """Read an upload with an extension allow-list and a hard size limit."""
    filename = upload.filename or ""
    extension = Path(filename).suffix.lower().lstrip(".")
    allowed = {item.lower().lstrip(".") for item in allowed_extensions}
    if extension not in allowed:
        raise HTTPException(status_code=400, detail="Unsupported upload type")

    chunks: list[bytes] = []
    total = 0
    while chunk := await upload.read(1024 * 1024):
        total += len(chunk)
        if total > MAX_UPLOAD_BYTES:
            raise HTTPException(status_code=413, detail="Uploaded file exceeds the size limit")
        chunks.append(chunk)
    return b"".join(chunks)
