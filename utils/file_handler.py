"""
File Handler Utilities for AGRI-MITRA
Provides safe filesystem access and path resolution.
"""

from pathlib import Path
from werkzeug.utils import secure_filename


def ensure_directory(path: Path) -> Path:
    """Ensures a directory exists on the filesystem."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def safe_filename_for_export(base_name: str, ext: str = 'csv') -> str:
    """Returns a sanitized filename with timestamp."""
    from datetime import datetime
    clean = secure_filename(base_name)
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    return f"{clean}_{timestamp}.{ext}"
